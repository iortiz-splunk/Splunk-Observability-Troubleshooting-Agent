# get-alerts-or-incidents — Reference

Full response shape and parameter details. Use when the agent needs to interpret unknown fields or add new output columns.

## AugmentedAlert (full field list)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Alert event ID |
| `eventId` | string | Event identifier |
| `active` | boolean | Whether the alert is currently active |
| `anomalyState` | string | e.g. `"anomalous"`, `"ok"` |
| `anomalyStateUpdateTimestampMs` | integer | Last state change (epoch ms) |
| `anomaly_state_update_iso_8601_date_time` | string | Timestamp for display |
| `detectLabel` | string | Detector label (use for "detector name") |
| `detector` | string | Detector display name |
| `detectorId` | string | Detector ID |
| `eventCategory` | string | e.g. `"ALERT"` |
| `incidentId` | string | Incident ID |
| `severity` | string | Critical, Major, Minor, Warning, Info |
| `priority` | integer | Numeric priority |
| `originatingMetric` | string \| null | Metric that triggered the alert |
| `muted` | boolean | Whether the alert is muted |
| `customProperties` | object \| null | Dimensions (host.name, k8s.pod.name, etc.) |
| `link` | `{ text, url }` | Link to detector/incident in UI |

## Parameters (detailed)

- **time_range**: Required. `start`/`stop` accept ISO-8601, relative durations (`-15m`, `-1h`, `-1d`, `-1w`), or POSIX timestamp. Relative is delta from `stop`; `stop` defaults to `now`.
- **service_name**: Use exact APM/RUM service name; do not use `keywords` for service names.
- **keywords**: Limit to 1–2 single words; if no results, retry without keywords.
