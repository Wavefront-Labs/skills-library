---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.canary-population-selection-and-sizing
name: canary-population-selection-and-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [canary-population, canary-sizing, canarying, progressive-delivery, argo-rollouts, release-engineering]
level: practitioner
status: docs-checked
description: "Choose canary size, duration and population so the canary is representative and statistically able to detect regressions, while limiting blast radius to the error budget."
sources: ["https://sre.google/workbook/canarying-releases/", "https://argo-rollouts.readthedocs.io/en/stable/features/canary/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canary population selection and sizing

Workbook "Canarying Releases": the canary must be large and long enough to surface problems, small enough
to limit damage, and representative of the full population. It also must run concurrently with a control.

## Size
- Blast radius: a canary at 5% that fails completely for 30 min costs `0.05 * 30 = 1.5` full-outage
  minutes. Make sure that fits in the error budget you are willing to spend per release.
- Signal: the canary must be sizeable and last long enough to be representative; stopping after a handful of
  queries gives no useful signal. The higher the processing rate, the less time a representative sample needs,
  and the more homogeneous the requests, the less traffic you need. Low-traffic services need longer or bigger canaries.
- Dilution: the Workbook's example is a 5% canary running a 20% error rate, which monitoring of the whole system
  sees as only a 1% error rate. Compare canary signals with a control, not the whole fleet.

## Duration
- Long enough to cover the slowest-appearing failure you expect (memory leaks, daily batch interactions,
  cache expiry).
- Multi-stage rollouts (small, then larger) are common; pick the stages from your error budget.

## Population
- **Representative**: cover each region/zone and client type; a canary only in one zone misses
  locale-specific bugs.
- **Control group**: compare the canary with a control population running the old version, not with the whole
  fleet. The Workbook warns that outliers (oversubscribed machines, different kernels, overloaded network
  segments) make canary-versus-control differences partly a function of the infrastructure, and that imperfect
  isolation lets a bad canary harm the control, so also check absolute measures such as SLOs.

## Argo Rollouts example
```yaml
strategy:
  canary:
    steps:
    - setWeight: 10
    - pause: { duration: 10m }
    - setWeight: 20
    - pause: {}   # pause indefinitely until promoted
```

## Gotchas
- Canarying on internal or employee traffic only is a dogfood stage, not a representative canary.
- Overlapping canaries of different changes confound the analysis; serialise or isolate.

## Checked

2026-11-01. Confirmed against the Workbook chapter Canarying Releases (size and duration, representativeness,
control comparison, the 5% canary at a 20% error rate, imperfect isolation) and the Argo Rollouts canary page
(steps, setWeight, pause with duration or indefinite). The 1.5 full-outage-minute figure is arithmetic. Removed:
the sample-size formula and example, the 1-5% typical range, the staged percentages, stickiness and the Istio
traffic-routing lines (not on the pages read).
Method: documentation only; no commands were run.

## Verify
- [ ] Sample size check done for the target metrics.
- [ ] Control group exists with matching size and start time.
