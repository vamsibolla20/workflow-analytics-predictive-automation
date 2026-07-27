from __future__ import annotations

from pathlib import Path
import pandas as pd

INVALID_ID = "00000000-0000-0000-0000-000000000000"


def load_json_events(*paths: str | Path) -> pd.DataFrame:
    """Load one or more JSON event files and merge them into one DataFrame."""
    frames = [pd.read_json(Path(path)) for path in paths]
    if not frames:
        raise ValueError("At least one JSON path is required.")
    return pd.concat(frames, ignore_index=True)


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean event-log data using the same broad ETL logic demonstrated in the
    original project, but without relying on any client-specific fields.
    """
    required = {
        "_id", "addedAtUtc", "functionName", "eventName", "userId",
        "flowId", "flowOriginId", "companyId", "dianaResourceId", "stepId"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.drop_duplicates(subset="_id", keep="first").copy()

    # Keep start/submit events. End events are represented by eventName == "end"
    # on submit records in the original project structure.
    out = out[out["functionName"].isin(["start", "submit"])].copy()

    out["datetime"] = pd.to_datetime(out["addedAtUtc"], utc=True, errors="coerce")
    out = out.dropna(subset=["datetime"])

    mask_invalid = out.astype(str).apply(
        lambda col: col.str.contains(INVALID_ID, regex=False)
    ).any(axis=1)
    out = out[~mask_invalid].copy()

    return out.reset_index(drop=True)


def add_dummy_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Create privacy-safe sequential dummy identifiers for portfolio analysis."""
    out = df.copy()

    mappings = {
        "userId": ("user_dummy", "USER"),
        "environmentId": ("environment_dummy", "ENV"),
        "companyId": ("company_dummy", "COMPANY"),
        "dianaResourceId": ("resource_dummy", "WORKITEM"),
        "stepId": ("step_dummy", "STEP"),
        "flowId": ("flow_dummy", "FLOW"),
        "flowOriginId": ("flow_origin_dummy", "FLOW_ORIGIN"),
    }

    for source, (target, prefix) in mappings.items():
        if source not in out.columns:
            continue
        unique_values = pd.Series(out[source].dropna().unique())
        mapping = {
            value: f"{prefix}_{idx}"
            for idx, value in enumerate(unique_values, start=1)
        }
        out[target] = out[source].map(mapping)

    return out


if __name__ == "__main__":
    sample = Path(__file__).resolve().parents[1] / "sample_data" / "synthetic_events.json"
    raw = load_json_events(sample)
    cleaned = clean_events(raw)
    anonymised = add_dummy_ids(cleaned)
    print(anonymised.head())
