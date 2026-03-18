#!/usr/bin/env python3
"""
Parse search_alerts_or_incidents MCP response and print a markdown table.

Usage:
  python parse_alerts_response.py [--truncate N] [path/to/response.json]
  python parse_alerts_response.py [--truncate N] < path/to/response.json

Options:
  --truncate N   Truncate Description (Context) column to N chars (default: no truncation).

Output: markdown table with columns
  timestamp | detector name | status | Severity | Description (Context)
"""

import argparse
import json
import sys

DESCRIPTION_KEYS = ["host.name", "k8s.pod.name", "k8s.container.name", "state"]


def build_description(a, truncate=None):
    """Build Description (Context) from eventCategory, metric, and key dimensions."""
    parts = []
    if a.get("eventCategory"):
        parts.append(a["eventCategory"])
    if a.get("originatingMetric"):
        parts.append("metric: " + a["originatingMetric"])
    cp = a.get("customProperties") or {}
    for k in DESCRIPTION_KEYS:
        if cp.get(k):
            parts.append(f"{k}={cp[k]}")
    out = "; ".join(parts) if parts else (a.get("link") or {}).get("text") or "-"
    if truncate and len(out) > truncate:
        out = out[: truncate - 3].rstrip() + "..."
    return out


def parse_alerts_to_rows(data, truncate=None):
    """Parse MCP search_alerts_or_incidents response into table rows."""
    alerts = data.get("alerts", [])
    rows = []
    for a in alerts:
        ts = a.get("anomaly_state_update_iso_8601_date_time", "")
        name = a.get("detectLabel") or a.get("detector", "")
        status = "Active" if a.get("active") else "Inactive"
        if a.get("anomalyState"):
            status = f"{status} ({a['anomalyState']})"
        sev = a.get("severity", "")
        ctx = build_description(a, truncate=truncate)
        rows.append((ts, name, status, sev, ctx))
    return rows


def main():
    parser = argparse.ArgumentParser(description="Format search_alerts_or_incidents response as markdown table")
    parser.add_argument("--truncate", type=int, default=None, metavar="N", help="Truncate Description column to N chars")
    parser.add_argument("file", nargs="?", default=None, help="JSON response file (default: stdin)")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    rows = parse_alerts_to_rows(data, truncate=args.truncate)
    print("| timestamp | detector name | status | Severity | Description (Context) |")
    print("|-----------|---------------|--------|----------|------------------------|")
    for r in rows:
        cells = [str(x).replace("|", "\\|") for x in r]
        print("| " + " | ".join(cells) + " |")
    print(f"\nTotal alerts: {len(rows)}")


if __name__ == "__main__":
    main()
