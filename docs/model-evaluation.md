# Model Evaluation

## Regularity Scoring

Regularity and automation scoring are descriptive heuristics designed to rank recurring workflow patterns.

They should be interpreted as decision-support indicators rather than guaranteed automation recommendations.

## Prophet

Forecast quality should be assessed using held-out history or rolling time-series validation before any operational use.

## LSTM

The example LSTM can be assessed with:

- Confusion matrix
- Precision
- Recall
- F1-score
- Threshold tuning

The threshold is configurable and defaults to `0.6` to reflect the original project's focus on balancing Start-event predictions.

## Deployment Considerations

Before production use:

- Validate against fresh data
- Monitor false-positive automation triggers
- Add human approval where needed
- Define failure handling and rollback procedures
- Monitor model drift
- Re-evaluate automation rules regularly
