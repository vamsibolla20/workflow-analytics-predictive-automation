from __future__ import annotations

import pandas as pd
from prophet import Prophet


def forecast_next_start(events: pd.Series, horizon_days: int = 30) -> pd.Timestamp:
    """
    Fit Prophet to synthetic/demo start timestamps and return the future timestamp
    with the highest predicted event intensity.

    This is a portfolio demonstration, not production scheduling logic.
    """
    timestamps = pd.to_datetime(events, utc=True).sort_values()
    if len(timestamps) < 5:
        raise ValueError("At least 5 events are required.")

    model_data = pd.DataFrame({
        "ds": timestamps.dt.tz_convert(None),
        "y": 1.0,
    })

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        interval_width=0.95,
    )
    model.fit(model_data)

    future = model.make_future_dataframe(periods=horizon_days * 24, freq="h")
    forecast = model.predict(future)

    last_event = model_data["ds"].iloc[-1]
    future_only = forecast[forecast["ds"] > last_event]
    if future_only.empty:
        raise RuntimeError("No future forecast rows were generated.")

    return future_only.loc[future_only["yhat"].idxmax(), "ds"]


def forecast_by_flow_user(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    starts = df[df["functionName"] == "start"].copy()

    for (flow_origin, user_id), group in starts.groupby(["flowOriginId", "userId"]):
        if len(group) < 5:
            continue
        try:
            next_run = forecast_next_start(group["datetime"])
            rows.append({
                "flowOriginId": flow_origin,
                "userId": user_id,
                "event_count": len(group),
                "next_predicted_run": next_run,
            })
        except Exception as exc:
            rows.append({
                "flowOriginId": flow_origin,
                "userId": user_id,
                "event_count": len(group),
                "next_predicted_run": pd.NaT,
                "error": str(exc),
            })

    return pd.DataFrame(rows)
