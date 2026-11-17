---
id: computing-software.cloud-infrastructure-engineering.google-cloud.slo-monitoring-and-error-budgets
name: slo-monitoring-and-error-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, slo, sli, error-budget, service-monitoring, burn-rate-alerts, availability-slo, latency-slo, request-based-sli, windows-based-sli, slo-api, custom-services, cloud-run-slo, gke-slo, sre, error-budget-policy, multi-window-burn-rate]
level: advanced
status: docs-checked
description: "Define SLIs and SLOs in Cloud Monitoring Service Monitoring: request- and window-based SLIs, error budgets, multi-window burn-rate alerts and error-budget policy."
sources: ["https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring", "https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/sli-metrics/overview", "https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate", "https://cloud.google.com/monitoring/service-monitoring/using-api", "https://sre.google/workbook/alerting-on-slos/", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SLO monitoring and error budgets

**Goal:** each user-facing service has 1-3 SLOs that reflect what users feel, an error
budget that is visible, and alerts that fire on *burn rate* rather than on every blip.

## 1. Choose SLIs (before touching the console)
| User journey | SLI |
|---|---|
| API call | **availability** = good requests / all requests (decide which status classes count as bad) |
| API call | **latency** = requests under X ms / all |
| Async job | **freshness** = outputs newer than N minutes |
| Data pipeline | **correctness/completeness** from a reconciliation metric |
Measure at the edge the user hits (load balancer or Cloud Run request metrics), not inside the service. Pick a goal the business will *defend*. An SLO should be no higher than necessary: a 100 % goal has no error budget. Keep the SLO tighter than any public or contractual commitment.

## 2. Create the service and SLO
Define the SLO with the Service Monitoring API (`services.serviceLevelObjectives`). A `ServiceLevelObjective` has:
- `goal` (fraction of good service; `0 < goal <= 0.9999`),
- one compliance period: `rollingPeriod` (a whole number of days, at most 30 days) or `calendarPeriod` (`DAY`, `WEEK`, `FORTNIGHT`, `MONTH`, ...),
- `serviceLevelIndicator`, which is either **request-based** or **windows-based**.

- **Request-based** (`requestBased`) counts good/total events (best for traffic): `goodTotalRatio` with `goodServiceFilter` / `badServiceFilter` and `totalServiceFilter` (Monitoring filters over two time series), or `distributionCut` with `distributionFilter` and a good `range` (for latency).
- **Windows-based** (`windowsBased`) marks each window good or bad: `windowPeriod` (at least 60 s, an integer fraction of a day) with `goodBadMetricFilter`, `goodTotalRatioThreshold`, `metricMeanInRange` or `metricSumInRange` (freshness, batch or low-traffic services).
- Rolling periods give a compliance measure every day; calendar periods give one score per period that matches billing periods.
- Time-series selectors for SLO data include `select_slo_burn_rate`; the alerting page lists the others. Alert policies on selectors other than burn rate must be created with the API.
- Error budget = (1 - goal) x eligible events in the compliance period.

## 3. Burn-rate alerts (multi-window)
Burn rate above 1 means that, if the measured error rate is sustained, the service will be out of SLO for the period. The SRE Workbook recommends these starting points for paging and ticketing (appropriate numbers depend on the service):
| Notify | Budget consumed | Window | Burn rate |
|---|---|---|---|
| page | 2 % | 1 hour | 14.4 |
| page | 5 % | 6 hours | 6 |
| ticket | 10 % | 3 days | 1 |
Build the condition on `select_slo_burn_rate("<SLO resource name>", "<lookback>")` with a threshold and duration (see the burn-rate alerting page), and pair each long window with a shorter one so the alert resets quickly once the burn stops (see "Multiple Burn Rate Alerts" in the Workbook chapter). Attach documentation to the policy that says what triggered it.

## 4. Error-budget policy (the human part)
Write it down and have leadership sign: when the compliance-period budget is **exhausted**, the team freezes feature launches and works reliability; when it is **healthy**, risky changes are allowed. Review budget consumption in the weekly ops review; attribute burn to incidents. Without the policy, SLOs are dashboards nobody looks at.

## Gotchas
- Decide deliberately whether client errors (4xx) count as bad; counting them makes clients' bugs your outage.
- Load-balancer request metrics can include health checks and bots; filter where possible.
- Rolling SLOs need a full period of data to be meaningful: set them up before launch.
- Low-traffic services are noisy with short windows; prefer a windows-based SLI or longer windows.
- Changing an SLO's goal or SLI creates a discontinuity: create a new SLO id and keep the old one for a while.

## Verify
- [ ] The Services page shows the SLO and its error budget; injecting a known error rate moves the budget visibly.
- [ ] A fast-burn alert fires on a sustained 100 % error injection and resolves shortly after it stops.
- [ ] The error-budget policy is linked from the SLO's description and was used (or explicitly not needed) last quarter.
- [ ] A burst of client-error responses that you decided not to count does not move the availability SLO.

## Checked
2026-10-31. Confirmed against the Cloud Monitoring SLO pages (concepts, using the API, burn-rate alerting), the SRE Workbook "Alerting on SLOs" chapter (2 % in 1 h / burn rate 14.4, 5 % in 6 h / 6, 10 % in 3 d / 1) and the Monitoring API v3 discovery document (`goal` bound, `rollingPeriod` up to 30 days, `calendarPeriod` values, `RequestBasedSli`, `WindowsBasedSli`, `TimeSeriesRatio`, `DistributionCut` fields).
Removed as unconfirmed: the Terraform and alert-policy HCL examples and resource names, the auto-discovered service list, the "no stable gcloud surface" statement, MQL selector names other than `select_slo_burn_rate`, the 7/28/30 rolling-period list, table SLO targets, the five-minute-window and requests-per-second advice, and the BigQuery export suggestion.
Method: documentation only; no commands were run.
