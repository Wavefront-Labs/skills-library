---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets
name: slos-and-error-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, slo, sli, sla, error-budget, error-budget-policy, burn-rate, multiwindow-alerts, multi-burn-rate, availability, latency-slo, rolling-window, request-based-sli, prometheus, sloth, pyrra, openslo, nines, alerting, on-call]
level: advanced
status: docs-checked
description: "Define SLIs users feel, set SLOs with explicit budget math, adopt an error-budget policy, and page with multiwindow multi-burn-rate alerts (14.4x/1h, 6x/6h, 1x/3d)."
sources: ["https://sre.google/sre-book/service-level-objectives/", "https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/alerting-on-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLOs and error budgets — measure what users feel, alert on budget burn

**Goal:** a small set of SLOs that reflect user happiness, an agreed policy for what
happens when budget runs out, and alerts that page for real budget threats with
almost no false pages.

## 1. Choose SLIs
SLI = good events / valid events, expressed as a ratio.
- **Availability:** non-5xx responses / all responses (decide deliberately how to count 4xx).
- **Latency:** requests faster than a threshold / all requests, e.g. `< 300 ms`. Use a
  threshold, not a mean; often several targets at different percentiles.
- **Freshness / correctness / throughput** for pipelines: records processed within 15 min.
- Measure as close to the user as practical: load balancer logs > server metrics;
  synthetic probes cover zero-traffic periods.

## 2. Set the SLO and do the math
Budget = (1 − SLO) × window. For a 30-day rolling window:

| SLO | Bad fraction | Budget (time-equivalent) |
|---|---|---|
| 99% | 1% | 7.2 h |
| 99.5% | 0.5% | 3.6 h |
| 99.9% | 0.1% | 43.2 min |
| 99.95% | 0.05% | 21.6 min |
| 99.99% | 0.01% | 4.32 min |

- Start from what users tolerate and what you achieved historically; don't promise more
  than your dependencies give (a service on a 99.95% database cannot sensibly be 99.99%).
- Request-based SLOs count events (a 10-minute outage at 3 a.m. costs less than at noon),
  which matches user experience better than time-slice uptime.
- SLA (contract with penalties) should be looser than the SLO.
- Pick a rolling window for alerting (the table below uses 30 days) and report on whatever calendar suits your reviews.

## 3. Error budget policy (written, signed by product and engineering)
- Budget remaining: ship freely; spend it on experiments and risky migrations.
- Budget exhausted over the window: freeze non-reliability feature launches until back
  within SLO; postmortem for any single incident that consumes a large share of the budget
  (set your own threshold); reliability work prioritised next sprint.
- Escalation path when the teams disagree. Without this policy, SLOs are just dashboards.

## 4. Burn-rate alerting
Burn rate = observed error ratio / (1 − SLO). Burn 1 spends exactly the budget over the window.
For 99.9% (budget ratio 0.001), from the SRE Workbook:

| Severity | Long window | Short window | Burn rate | Error ratio > | Budget spent at trigger |
|---|---|---|---|---|---|
| Page | 1 h | 5 m | 14.4 | 1.44% | 2% |
| Page | 6 h | 30 m | 6 | 0.6% | 5% |
| Ticket | 3 d | 6 h | 1 | 0.1% | 10% |

Both windows must exceed the threshold: the long one proves significance, the short one
makes the alert reset quickly once fixed.
```yaml
- alert: SLOBurnFast
  expr: |
    (job:slo_errors:ratio_rate1h{job="api"} > (14.4 * 0.001)
      and job:slo_errors:ratio_rate5m{job="api"} > (14.4 * 0.001))
    or
    (job:slo_errors:ratio_rate6h{job="api"} > (6 * 0.001)
      and job:slo_errors:ratio_rate30m{job="api"} > (6 * 0.001))
  labels: {severity: page}
```
Generate the recording rules from an SLO spec rather than hand-writing them for every service.

## 5. Operate it
- Weekly: budget remaining per SLO, top budget consumers (incidents, deploys, dependencies).
- Quarterly: revisit targets — an SLO never at risk is too loose or the wrong SLI; one
  constantly blown needs investment or an honest lower target.

## Gotchas
- Low-traffic services: 1 error in 50 requests is a 2% error ratio and fires a 14.4x page.
  Add a minimum-request guard, synthetic traffic, or longer windows.
- Averaging per-instance ratios is wrong; sum good and total events first, then divide.
- Counting 4xx as bad punishes you for client bugs; counting none hides your own 404 regressions — pick deliberately.
- 100% is never the right target; it forbids change and your users' networks are worse anyway.
- Planned maintenance still burns budget unless the policy explicitly excludes it.

## Verify
- [ ] Each user-facing service has 1-3 SLIs defined as good/valid event ratios.
- [ ] Budget for each SLO is stated in both ratio and time-equivalent terms.
- [ ] A written error-budget policy exists and has been invoked or reviewed in the last quarter.
- [ ] Page alerts use both long and short windows with the 14.4x and 6x thresholds (or justified alternatives).
- [ ] Low-traffic services have a guard against single-request pages.
- [ ] A budget dashboard shows remaining budget per service over the rolling window.

## Checked
2026-11-01. Confirmed in the SRE Workbook Alerting on SLOs: the multiwindow multi-burn-rate table (2% in 1 hour = 14.4, 5% in 6 hours = 6, 10% in 3 days = 1; short windows 5 minutes, 30 minutes, 6 hours), both-window rule for fast reset, and the low-traffic caveat. Budget arithmetic recomputed. Removed the Sloth, Pyrra and OpenSLO names, the 429 rule, the 28-day window claim, the 20% postmortem threshold as a Google figure and the histogram bucket claim; the latency percentile example was also dropped. Other advice here is judgement, not sourced.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-and-alert-rules, computing-software.cloud-infrastructure-engineering.observability.instrumentation-strategy
