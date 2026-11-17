---
id: computing-software.cloud-infrastructure-engineering.azure.front-door-logs-metrics-and-reports
name: front-door-logs-metrics-and-reports
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, front-door, afd-logs, frontdooraccesslog, origin-health, cache-hit-ratio, afd-reports]
level: practitioner
status: docs-checked
description: "Monitor Azure Front Door Standard/Premium: access, health probe and WAF logs, key metrics (origin health, latency, 4xx/5xx, byte hit ratio), built-in reports and KQL."
sources: ["https://learn.microsoft.com/azure/frontdoor/front-door-diagnostics", "https://learn.microsoft.com/azure/frontdoor/standard-premium/how-to-reports", "https://learn.microsoft.com/azure/frontdoor/monitor-front-door-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Front Door logs, metrics and reports

**Goal:** separate "Front Door problem" from "origin problem" from "cache problem" in minutes.

## Metrics
| Metric | Watch for |
|---|---|
| Request Count (split by HTTP status group, client country, endpoint) | Traffic shape |
| Percentage 4XX / 5XX | Spikes - 5XX from origin vs edge |
| Origin Health Percentage (split by origin) | Probe failures |
| Origin Latency vs Total Latency | Slow origin vs slow edge/client |
| Byte Hit Ratio | Caching effectiveness |
Metric names: `RequestCount`, `Percentage4XX`, `Percentage5XX`, `OriginHealthPercentage` (split by Origin and OriginGroup),
`OriginLatency`, `TotalLatency`, `ByteHitRatio` (per Endpoint). Alert on 5XX percentage, origin health below 100 per
origin group, and a byte hit ratio drop after a release; pick thresholds from your own baseline.

## Logs (diagnostic settings on the profile)
Categories: **FrontDoorAccessLog**, **FrontDoorHealthProbeLog**, **FrontDoorWebApplicationFirewallLog**.
Run KQL against `AzureDiagnostics` filtered on `Category == "FrontDoorAccessLog"`. Useful fields (the access log
reference lists them; in `AzureDiagnostics` they carry type suffixes such as `_s` or `_b`, so inspect a row first):
`HttpStatusCode` (0 when the origin timed out), `CacheStatus`, `OriginName`, `TimeTaken` (seconds, edge receive to last
byte sent to the client), `TrackingReference` (the `X-Azure-Ref` header sent to clients and origins; ask users for it).
Health probe logs show per-origin probe results.

## Built-in reports
Profile > Reports: key metrics, traffic by location, top URLs, referrers and user agents (top 50 each, with cache hit
ratio and status code distribution), plus a Security report with WAF rule matches (Premium tier only). Reports are free,
mostly built on access log data, and need no extra configuration; they can be downloaded as CSV.

## Triage pattern
1. User provides `X-Azure-Ref` -> find the access log entry.
2. 5xx with `CacheStatus` MISS and high `OriginLatency` -> origin. 403 with a WAF log match -> WAF rule.
3. Origin health < 100 -> probe path/host header/private link approval.

## Verify
- [ ] Alerts in place; a test request's `X-Azure-Ref` is findable in the access log.

## Checked
2026-10-28. Confirmed in Learn `monitor-front-door-reference`, `front-door-diagnostics` and `how-to-reports`: metric names and
dimensions, log category names, AzureDiagnostics destination, HttpStatusCode/TimeTaken/TrackingReference semantics, the
X-Azure-Ref header, report contents, Premium-only security reports, free reports and CSV download. Removed: the sample KQL
(its `_s` column names were not confirmed), the 5 percent / 5 minute alert threshold, the pop and requestUri fields, the
Basic/Auxiliary table plan tip and the probe load gotcha.
Method: documentation only; no commands were run.
