---
id: computing-software.systems-network-administration.patch-management.canary-analysis-for-patch-rollouts
name: canary-analysis-for-patch-rollouts
category: computing-software
field: systems-network-administration
product: patch-management
tags: [canary-analysis, canary, kayenta, patch-testing, sre, patch-management]
level: practitioner
status: docs-checked
description: "Judge a patch canary objectively: choose metrics, compare canary against a control population, set pass/fail thresholds before rollout, and automate with Argo Rollouts analysis."
sources:
  - https://spinnaker.io/docs/guides/user/canary/
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
  - https://sre.google/workbook/canarying-releases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canary analysis for patch rollouts

Automated canary analysis partially rolls out a change, then evaluates it against the
current deployment. Define the metrics and the acceptable behaviour **before** patching, so
the decision is not "looks fine on the dashboard".

## Canary and control
- Canary: the subset that gets the change. Control: the rest, still on the old version.
- The canary only needs to be large enough to detect key critical conditions, but it must be
  sizeable and long enough to be representative of the whole deployment. A handful of
  requests gives no useful signal.
- In a large population there are outliers (oversubscribed machines, different kernels,
  overloaded network segments), so the canary-versus-control difference is not purely your
  change. A bigger canary reduces this problem.
- Canary and control may share backends or networks; a bad canary can affect the control.
  Also check absolute measures such as SLOs, not only the A/B difference.
- Before/after comparison (replace everything, compare with earlier) is risky because time
  itself changes metrics, for example a business day versus a weekend.

## Choosing metrics
- Start from your SLIs: failed requests and latency usually map best to user-visible
  problems. Resource metrics such as CPU are noisier and can make the canary flaky enough
  that operators ignore it.
- Stack-rank metrics and keep only the top few (the SRE workbook suggests perhaps no more
  than a dozen).
- Metrics must be attributable to the change. Whole-host CPU is a poor metric if other
  processes can move it.
- Too strict a definition of acceptable gives false positives; too loose lets bad canaries
  through. Revisit the thresholds as the service changes.
- Your monitoring must break metrics down by canary versus control; a whole-service average
  hides a bad 5% canary.
- Metric aggregation windows should be no longer than the canary duration.

## Duration and timing
- Choose canary duration to fit release cadence; run one canary at a time.
- Performance defects usually appear under heavy load, so an off-peak canary may miss them.
- For batch or pipeline systems the canary must span at least one work unit, with a work
  unit always handled by workers from the same pool (canary or control).
- A gradual canary uses stages: a small first stage judged on clear signals (crashes,
  failures), then a larger stage.

## Automating with Argo Rollouts
An `AnalysisTemplate` metric has `interval`, `count`, `successCondition`, `failureLimit`
and a `provider`. Example using Prometheus (address is a placeholder):
```yaml
metrics:
- name: error-rate
  interval: 5m
  count: 6
  successCondition: result[0] < 0.01
  failureLimit: 1
  provider:
    prometheus:
      address: http://prometheus.example.com:9090
      query: sum(rate(http_requests_total{job="app",status=~"5..",track="canary"}[5m])) / sum(rate(http_requests_total{job="app",track="canary"}[5m]))
```
Prometheus queries return a vector, hence `result[0]`. With `count` and `interval` several
measurements are taken over time; without them a single measurement is taken.

## Verify
Save the canary report with the change record: metrics, windows, outcome, decision and who
decided.

## Checked
2026-11-08. Confirmed against the Google SRE Workbook chapter "Canarying Releases"
(population, duration, load, metric selection, attribution, before/after risk, isolation,
monitoring breakdown, aggregation window, noninteractive systems, gradual canary) and the
Argo Rollouts analysis page (`interval`, `count`, `successCondition`, `failureLimit`,
Prometheus provider, vector result). The Spinnaker page is only an index and confirms the
partial-rollout-then-evaluate definition. Removed: Kayenta scoring details and thresholds
(Mann-Whitney U, 95/75), the 1-5% sizing, the 1.2x ratio rule, and fixed 24 h and 30-60 min
durations, none of which the pages state.
Method: documentation only; no commands were run.
