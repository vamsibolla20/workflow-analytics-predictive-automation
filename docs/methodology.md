# Methodology

## ETL

The portfolio implementation follows the broad analytical workflow used in the original project:

1. Load event-log JSON files into pandas.
2. Merge event sources.
3. Remove duplicate events using the event identifier.
4. Convert event timestamps to datetime.
5. Remove invalid placeholder IDs.
6. Filter to relevant workflow events.
7. Create dummy identifiers where needed for privacy-safe analysis.

## Descriptive Analysis

Workflow activity can be analysed by:

- Hour of day
- Day of week
- Event type
- Workflow/user combination

The original project used these views to understand how workflow activity was distributed before modelling.

## Regularity Analysis

The core regularity logic uses:

- Day consistency
- Time consistency
- Interval adherence

Intervals are classified broadly as:

- Daily: under 36 hours
- Weekly: under 10 days
- Monthly: under 45 days
- Longer: above 45 days

These windows allow some timing irregularity rather than requiring exact calendar recurrence.

## Prophet

Prophet is included as a time-series forecasting option for recurring start-event patterns.

The public code uses only synthetic timestamps.

## LSTM

The LSTM example uses sequences of three prior workflow events and the features:

- Encoded step ID
- Encoded work-item/resource ID
- Time difference between events

The target is whether the next event is a Start event.

## Automation Layer

The original project explored using predictions to trigger workflows through an API.

The public portfolio intentionally stops at a safe interface layer and does not contain:

- Client API endpoints
- Tokens
- API keys
- User identifiers
- Environment identifiers
- Real workflow IDs
