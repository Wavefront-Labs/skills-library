---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.anomaly-kpis
name: anomaly-kpis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, anomaly-management, anomaly-kpis, finops-kpis, time-to-detect, time-to-resolve, false-positive-rate]
level: practitioner
status: docs-checked
description: "Measure anomaly management: time to detect, acknowledge and resolve, cost impact avoided, false-positive rate and coverage, with a log schema and monthly review."
sources: ["https://www.finops.org/framework/capabilities/anomaly-management/", "https://www.finops.org/wg/finops-kpis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anomaly management KPIs

Without measurement, anomaly management decays into ignored alerts. Log every anomaly and track a
handful of KPIs.

## Log schema (one row per anomaly)
`id, detected_at, source (native/custom/human), owner, service, start_of_spend, acknowledged_at,
resolved_at, baseline_per_day, peak_per_day, total_excess_cost, classification (true/false
positive, expected), cause_category (config, runaway, security, pricing, data issue), preventive_action`.

## KPIs
| KPI | Formula | In the FinOps Anomaly Management page? |
|---|---|---|
| Time to detect (TTD) | detected_at - start_of_spend, averaged per week or month | yes: mean time to detect |
| Time to acknowledge | acknowledged_at - detected_at | yes: mean time to notify owner (until the owner acknowledges) |
| Time to resolve (TTR) | resolved_at - detected_at | yes, as duration of unresolved anomalies and time to investigate and address |
| Excess cost | sum(total_excess_cost) per month | yes: amount of cost associated with anomaly alerts |
| Avoided cost | (expected duration without action - actual duration) x excess/day, to the next billing period | yes: spending amount avoided, to nearest following billing period |
| False-positive rate | false positives / alerts | yes: anomalies vs missed vs false positives; unactionable counts by category |
| Coverage | spend under an active monitor / total spend | no; the page asks engineers to give feedback on detection coverage |
| Repeat rate | anomalies with a cause seen before / total | no; own KPI |

The page publishes no numeric targets, so set your own and record them in the KPI definition. It also lists
count of anomalies per period, alerts suspended or ignored by team, and percentage of anomalies handled by automation.

## Steps
1. Create the log (ticket type in the ITSM tool or a table fed by alert bots).
2. Owners classify and close each anomaly; FinOps reviews unclassified items weekly.
3. Monthly review: KPIs, top causes, preventive actions (budget actions, quotas, policies) and
   threshold tuning.
4. Report TTD and excess cost in the month-end pack.

## Gotchas
- TTD measured from alert time instead of spend start hides slow detection.
- Avoided-cost estimates inflate easily; cap the assumed duration, as the FinOps page does by counting avoided spend only to the nearest following billing period.
- A falling alert count can mean thresholds were loosened; watch coverage and TTD together.

## Verify
- [ ] Every alert has a classification within an agreed deadline.
- [ ] KPIs reported monthly with trend.

## Checked
Date: 2026-11-08. Confirmed against the FinOps Anomaly Management capability page (measures of success list). The
FinOps KPIs library page is a dynamic list and its individual KPI entries were not readable, so only the Anomaly
Management page was used for KPI names. Removed the invented numeric targets (24-48 h, 3 days, 30-50 percent, 90 percent).
Method: documentation only; no commands were run.
