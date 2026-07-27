# Workflow Analytics & Predictive Automation

## Project Overview

This portfolio project demonstrates how historical workflow event data can be analysed to identify recurring patterns, predict future workflow starts, and support workflow automation.

The repository is based on a university industry project involving event-log analysis, regularity scoring, Prophet forecasting, LSTM modelling, and an API-based workflow automation concept.

This public version contains **no client data, credentials, production identifiers, or proprietary records**. It uses synthetic example data and portfolio-safe code only.

## Business Objective

The project explores how workflow event history can be used to:

- Understand when and how workflows are typically started
- Identify recurring workflow patterns
- Score workflows for automation potential
- Predict future start activity
- Support automated workflow triggering through an API integration pattern

## Analytical Approach

1. **Data preparation**
   - Load JSON event logs
   - Merge event sources
   - Remove duplicates
   - Convert timestamps
   - Remove invalid placeholder IDs
   - Filter relevant events

2. **Descriptive workflow analysis**
   - Analyse event activity by weekday and hour
   - Compare Start, Submit, and End event behaviour

3. **Regularity analysis**
   - Measure day consistency
   - Measure time consistency
   - Measure interval adherence
   - Produce a workflow regularity / automation score

4. **Forecasting**
   - Use Prophet-style forecasting logic for recurring workflow timing

5. **Sequence modelling**
   - Use an LSTM model to classify future events as Start vs Not Start from recent workflow sequences

6. **Automation pattern**
   - Use model outputs to determine candidate start times
   - Pass approved workflow IDs and schedules into an API-triggering layer

## Repository Structure

```text
workflow-analytics-predictive-automation-safe/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── data_preparation.py
│   ├── regularity_analysis.py
│   ├── prophet_forecasting.py
│   ├── lstm_model.py
│   └── automation_scheduler.py
├── sample_data/
│   └── synthetic_events.json
├── docs/
│   ├── methodology.md
│   ├── data-dictionary.md
│   ├── model-evaluation.md
│   └── privacy-and-safety.md
├── notebooks/
│   └── README.md
└── images/
    └── README.md
```

## Example Data

The included dataset is synthetic and designed only to demonstrate the repository workflow.

It includes fields such as:

- `addedAtUtc`
- `functionName`
- `eventName`
- `userId`
- `flowId`
- `flowOriginId`
- `companyId`
- `dianaResourceId`
- `stepId`

The values do not come from the original client system.

## Skills Demonstrated

- Python
- pandas
- NumPy
- Workflow Analytics
- Event Log Analysis
- Business Process Analysis
- Time-Series Analysis
- Predictive Modelling
- LSTM
- Prophet
- Model Evaluation
- Automation Opportunity Analysis
- API Integration Design
- Data Privacy & Portfolio Sanitisation

## Important Note

The original university project included real client event logs and API configuration. Those elements are intentionally excluded here.

This repository is a **sanitised portfolio reconstruction** that demonstrates the analytical methods and technical approach without exposing confidential or client-specific information.
