from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense


def prepare_lstm_dataset(df: pd.DataFrame, window_size: int = 3):
    events = df[
        (df["functionName"] == "start") | (df["eventName"].str.lower() == "end")
    ].copy()

    step_encoder = LabelEncoder()
    resource_encoder = LabelEncoder()

    events["step_encoded"] = step_encoder.fit_transform(events["stepId"].astype(str))
    events["resource_encoded"] = resource_encoder.fit_transform(
        events["dianaResourceId"].astype(str)
    )
    events["time_diff"] = (
        events.sort_values("datetime")
        .groupby("flowId")["datetime"]
        .diff()
        .dt.total_seconds()
        .fillna(0)
    )

    sequences, targets, metadata = [], [], []

    for flow_id, group in events.groupby("flowId"):
        group = group.sort_values("datetime").reset_index(drop=True)
        for i in range(len(group) - window_size):
            seq = group[
                ["step_encoded", "resource_encoded", "time_diff"]
            ].iloc[i:i + window_size].to_numpy(dtype=np.float32)

            next_row = group.iloc[i + window_size]
            target = 1 if next_row["functionName"] == "start" else 0

            sequences.append(seq)
            targets.append(target)
            metadata.append({
                "timestamp": next_row["datetime"],
                "flowId": flow_id,
                "workitem": next_row["dianaResourceId"],
            })

    if not sequences:
        raise ValueError("Not enough sequential events to build LSTM samples.")

    return (
        np.asarray(sequences, dtype=np.float32),
        np.asarray(targets, dtype=np.float32),
        pd.DataFrame(metadata),
    )


def train_lstm(
    X: np.ndarray,
    y: np.ndarray,
    threshold: float = 0.6,
    epochs: int = 5,
    batch_size: int = 32,
):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
    )

    model = Sequential([
        LSTM(64, input_shape=(X.shape[1], X.shape[2])),
        Dense(1, activation="sigmoid"),
    ])
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(X_test, y_test),
        verbose=0,
    )

    probabilities = model.predict(X_test, batch_size=batch_size, verbose=0).flatten()
    predictions = (probabilities > threshold).astype(int)

    return {
        "model": model,
        "threshold": threshold,
        "confusion_matrix": confusion_matrix(y_test, predictions),
        "classification_report": classification_report(
            y_test, predictions, zero_division=0
        ),
    }
