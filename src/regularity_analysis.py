from __future__ import annotations

from collections import Counter
import numpy as np
import pandas as pd


def classify_interval(mean_diff: pd.Timedelta) -> tuple[str, pd.Timedelta]:
    if mean_diff < pd.Timedelta(hours=36):
        return "Daily", pd.Timedelta(days=1)
    if mean_diff < pd.Timedelta(days=10):
        return "Weekly", pd.Timedelta(days=7)
    if mean_diff < pd.Timedelta(days=45):
        return "Monthly", pd.Timedelta(days=30)
    return "Longer", mean_diff


def calculate_regularity_metrics(group: pd.DataFrame) -> pd.Series:
    events = group["datetime"].sort_values()
    diffs = events.diff().dropna()

    if len(events) < 2 or diffs.empty:
        return pd.Series({
            "event_count": len(events),
            "mean_time_between_events_hours": np.nan,
            "interval": "Insufficient data",
            "day_consistency": np.nan,
            "time_consistency": np.nan,
            "interval_adherence": np.nan,
            "regularity_score": np.nan,
        })

    days = events.dt.dayofweek
    minutes = events.dt.hour * 60 + events.dt.minute
    rounded_15 = minutes.apply(lambda x: 15 * round(x / 15))

    day_consistency = Counter(days).most_common(1)[0][1] / len(days)
    time_consistency = Counter(rounded_15).most_common(1)[0][1] / len(rounded_15)

    mean_diff = diffs.mean()
    interval, expected = classify_interval(mean_diff)

    # Clip adherence to keep the score interpretable within 0-1.
    adherence = 1 - (np.abs(diffs - expected) / expected).mean()
    interval_adherence = float(np.clip(adherence, 0, 1))

    if interval == "Weekly":
        score = np.nanmean([day_consistency, time_consistency, interval_adherence])
    elif interval == "Daily":
        score = np.nanmean([time_consistency, interval_adherence])
    else:
        score = interval_adherence

    return pd.Series({
        "event_count": len(events),
        "mean_time_between_events_hours": mean_diff.total_seconds() / 3600,
        "interval": interval,
        "day_consistency": day_consistency,
        "time_consistency": time_consistency,
        "interval_adherence": interval_adherence,
        "regularity_score": float(score),
    })


def score_automation_candidates(df: pd.DataFrame, min_events: int = 5) -> pd.DataFrame:
    starts = df[df["functionName"] == "start"].copy()

    metrics = (
        starts.groupby(["flowOriginId", "userId"], group_keys=False)
        .apply(calculate_regularity_metrics)
        .reset_index()
    )

    metrics = metrics[metrics["event_count"] >= min_events].copy()
    metrics["automation_score"] = (
        0.6 * metrics["time_consistency"].fillna(0)
        + 0.2 * metrics["day_consistency"].fillna(0)
        + 0.2 * metrics["interval_adherence"].fillna(0)
    )
    return metrics.sort_values("automation_score", ascending=False)


if __name__ == "__main__":
    from pathlib import Path
    from data_preparation import load_json_events, clean_events

    sample = Path(__file__).resolve().parents[1] / "sample_data" / "synthetic_events.json"
    df = clean_events(load_json_events(sample))
    print(score_automation_candidates(df).head(10))
