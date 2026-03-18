---
name: get-alerts-or-incidents
description: Retrieves and formats alerts or incidents from Splunk Observability Cloud. Use when the user asks for alerts, incidents, detector triggers, or "what's firing" in O11y Cloud.
---

# Get Alerts or Incidents from Splunk Observability Cloud

Apply when the user wants alerts/incidents from Splunk Observability Cloud (list, filter by time/severity/service).

---

## Quick path (preferred)

1. **Call MCP:** `search_alerts_or_incidents`, server `user-o11y-mcp-server-us1`.
   - **params:** `time_range: { start: "-1h", stop: "now" }`, `include_inactive: true` (and optional `severity`, `service_name`, `detector_id`, `keywords`, `environments`).
2. **Format:** Run `python .cursor/skills/get-alerts-or-incidents/scripts/parse_alerts_response.py <response_file>` (or pipe JSON to stdin). Optionally use `--truncate 120` to shorten the Description column.

Output: markdown table with columns **timestamp | detector name | status | Severity | Description (Context)** and total count.

---

## MCP tool and parameters

| Parameter | Description |
|-----------|-------------|
| `time_range` | Required. `{ start, stop }` — e.g. `start: "-1h"`, `stop: "now"`. Use `-15m`, `-1h`, `-1d`, `-1w` for relative. |
| `include_inactive` | boolean; `true` to include resolved alerts. |
| `detector_id` | string \| null. Filter by detector ID. |
| `service_name` | string \| null. Exact APM/RUM service name (do not use `keywords` for services). |
| `keywords` | string[] \| null. 1–2 single words for detector label; retry without if no results. |
| `severity` | string[] \| null. `Critical`, `Major`, `Minor`, `Warning`, `Info`. |
| `environments` | string[] \| null. Filter by environment. |

---

## Column mapping (when not using the script)

Response: `{ "alerts": [ ... ] }`. Map each alert to one row:

| Column | Source field(s) |
|--------|-----------------|
| timestamp | `anomaly_state_update_iso_8601_date_time` |
| detector name | `detectLabel` or `detector` |
| status | `"Active" if active else "Inactive"` + `" (" + anomalyState + ")"` if present |
| Severity | `severity` |
| Description (Context) | Concatenate: `eventCategory`; `"metric: " + originatingMetric`; from `customProperties`: `host.name`, `k8s.pod.name`, `k8s.container.name`, `state`. Fallback: `link.text` or `"-"`. |

Escape `|` in cells as `\|`. Optionally truncate Description to ~120 chars.

---

## Expected output

```markdown
| timestamp | detector name | status | Severity | Description (Context) |
|-----------|---------------|--------|----------|------------------------|
| 2026-03-11T16:17:40+00:00 | Global - System Memory Usage - Critical | Active (anomalous) | Critical | ALERT; metric: system.memory.usage; host.name=... |
...
Total alerts: N
```

---

## More detail

- Full response schema and parameter notes: [reference.md](reference.md)
