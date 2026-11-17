---
id: computing-software.cloud-infrastructure-engineering.datadog.slos
name: slos
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, slo, service-level-objective, error-budget, burn-rate]
level: practitioner
status: docs-checked
description: "Create Datadog metric-based, monitor-based and time slice SLOs, set targets below 100 percent, read error budget and configure burn rate alerts."
sources: ["https://docs.datadoghq.com/service_level_objectives/", "https://docs.datadoghq.com/service_level_objectives/metric/", "https://docs.datadoghq.com/service_level_objectives/burn_rate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Level Objectives
Goal: track reliability against a target.

SLO types:
- Metric-based: count-based; SLI = sum of good events divided by good plus bad events (a legacy total-events form can only be created through the API).
- Monitor-based: time-based, from the uptime of a new or existing monitor; adjustments are made on the monitor.
- Time Slice: time-based, from a custom uptime definition (good time over total time), with no monitor needed.

Create: SLO manage page > New SLO, pick the type, set the target and a rolling window of 7, 30 or 90 days, then title, description, tags and save.

- Metric-based queries must use COUNT, RATE or percentile-enabled DISTRIBUTION metrics. For distributions use the `count values...` aggregator with a numeric threshold. Optional grouping: `sum by` for COUNT/RATE.
- Docs example: with a tag like `code:2xx`, good events are `sum:httpservice.hits{code:2xx} + sum:httpservice.hits{code:4xx}` and bad events are `sum:httpservice.hits{code:5xx}`; 3xx redirects are excluded so they count for neither side.
- Error budget = 100% minus target. Remaining budget (%) = 100 * (current status - target) / (100 - target).
- Targets must be strictly below 100%: a 100% target has zero error budget and causes division by zero in alert evaluation. Datadog recommends a target stricter than your SLA. Decimal places: up to three for metric-based; monitor-based up to two for 7 and 30 day, three for 90 day.
- Burn rate = how fast budget is consumed relative to the window: rate 1 uses the whole budget in exactly the window, rate 2 in half. Example from the docs: alert at 14.4 or more over the past hour and past 5 minutes for a 30-day target, with an optional warning at 7.2.
- Burn rate alert: set from Save and Set Alert or Set up Alerts on an SLO, Burn Rate tab. Long window 1 to 48 hours; short window is automatically 1/12 of the long window in the UI (other values via API or Terraform, always shorter than the long window). Threshold must satisfy 0 < burn rate <= 1 / (1 - target). It alerts only when both windows are at or above the threshold.
- Higher burn rates should be paired with shorter long windows.

Gotcha: pick the window you report on and keep it; the shortest window is selected by default.

## Verify
- The SLO list shows status and remaining error budget for the chosen window, and a burn rate alert is attached after saving.

## Checked
2026-11-03. Confirmed against the SLO overview, metric-based SLO and burn rate alert pages. Removed: the JSON body (`trace.http.request.hits.by_http_status` metric and field names not on the pages), "filter health checks" gotcha, the "several 9s need volume" claim, and meeting/process advice.
Method: documentation only; no commands were run.
