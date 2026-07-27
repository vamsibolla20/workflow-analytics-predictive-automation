# Data Dictionary

The synthetic demo dataset mirrors the structure needed for workflow analysis.

| Field | Description |
|---|---|
| `_id` | Unique synthetic event identifier |
| `addedAtUtc` | Event timestamp in UTC |
| `environmentId` | Synthetic environment identifier |
| `functionName` | Workflow action, such as `start` or `submit` |
| `eventName` | Used to mark end events in the demo |
| `userId` | Synthetic user identifier |
| `flowId` | Synthetic workflow-version identifier |
| `flowOriginId` | Synthetic identifier grouping workflow versions |
| `companyId` | Synthetic company identifier |
| `dianaResourceId` | Synthetic work-item identifier |
| `dianaResourceType` | Resource/work-item type |
| `stepId` | Synthetic workflow step identifier |

All values in `sample_data/synthetic_events.json` are generated solely for portfolio demonstration.
