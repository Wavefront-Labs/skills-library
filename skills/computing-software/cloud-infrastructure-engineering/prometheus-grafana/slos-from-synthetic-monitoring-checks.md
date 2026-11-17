---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.slos-from-synthetic-monitoring-checks
name: slos-from-synthetic-monitoring-checks
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-slo, synthetic-slo, synthetic-monitoring, probe-success, availability-sli]
level: advanced
status: docs-checked
description: "Build availability SLOs from Grafana Synthetic Monitoring checks using probe_success as an Advanced ratio SLI, with target and window rules."
sources: ["https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/analyze-results/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/create/", "https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/http/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLOs from synthetic checks

**Goal:** measure availability from the outside, including when there is no user traffic.

## Metrics
Synthetic Monitoring stores check results as Prometheus metrics and Loki logs. Common metrics: `probe_success`,
`probe_duration_seconds`, `probe_all_success`, `sm_check_info`. Metrics carry `job` (check job name), `instance`
(target) and `probe` (location) labels, plus any custom labels.

## SLI in Grafana SLO
- The SLI query must return a success ratio between 0 and 1 and, for all SLO features to work, be expressed as
  numerator / denominator. The Advanced query option is for custom queries; the SLO docs list "Probe availability
  (Prometheus binary gauge)" and "Probe latency (Prometheus gauge)" among the Advanced examples.
- Sketch of an availability SLI over `probe_success` (a 0/1 gauge), for one check:
```promql
sum(sum_over_time(probe_success{job="<JOB>", instance="<TARGET>"}[$__rate_interval]))
/
sum(count_over_time(probe_success{job="<JOB>", instance="<TARGET>"}[$__rate_interval]))
```
- Data sources: SLI queries run against a source data source (Mimir, Prometheus-compatible, Splunk, AppDynamics or
  Graphite); the target data source stores the recording rules and must be Mimir or Prometheus-compatible.
- Window and target: minimum window 7 days, default 28 days. The error budget is 100% minus the target (a 99.5%
  target leaves 0.5%). After you enter a target, Grafana SLO queries 90 days of history to predict the chance of meeting it.
- Alert rules: fast-burn alerts evaluate short periods and fire when the budget is consumed quickly; slow-burn alerts
  are the second type.
- Add team or service labels to the SLO; they can route alert notifications.

## Verify
- [ ] The SLI history matches known outages, and the predicted probability for the target is reasonable.

## Checked

2026-11-08. Confirmed against Grafana "Create SLOs" and the Synthetic Monitoring "Analyze results" and HTTP check
pages. The Google SRE workbook source was not read and is removed. Removed as unconfirmed: the latency PromQL
example, the events-per-day arithmetic and probe-count guidance, alert sensitivity advice, and the "keep targets
stable" note. The `probe_success` query is an illustration of the ratio form, not a documented query; test it in the
SLO query editor.
Method: documentation only; no commands were run.
