---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.headroom-and-utilisation-targets
name: headroom-and-utilisation-targets
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [headroom-policy, utilisation-targets, n-plus-2, capacity-planning, redundancy, promql]
level: practitioner
status: docs-checked
description: "Set headroom and target utilisation from N+2 redundancy and a load-tested breaking point, so the service survives losing units at peak."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://sre.google/sre-book/software-engineering-in-sre/", "https://sre.google/workbook/managing-load/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headroom and utilisation targets

Target utilisation is not a taste; derive it from a measured breaking point.

## Derivation
The SRE Book (Addressing Cascading Failures) couples capacity planning with performance testing to find the
load at which the service fails. Its example: every cluster's breaking point is 5,000 QPS, load is spread
evenly, and peak load is 19,000 QPS. Four clusters carry the peak (19,000 / 5,000 = 3.8), so approximately six
clusters are needed to run at N + 2.

```
units_needed_at_peak = ceil(peak_load / breaking_point_per_unit)
units_to_run         = units_needed_at_peak + k          # N+2 -> k = 2
steady_util_at_peak  = peak_load / (units_to_run * breaking_point_per_unit)
```
In the book's example that is 19,000 / 30,000, about 63% of the breaking point with all six clusters up, which
is what lets two clusters be lost and the rest still carry peak. Use a breaking point measured below the
latency or error limit you need, not the point where the process dies.

## Headroom policy (write it down)
State per service: the peak utilisation target, how many units it must survive losing at peak with latency
within SLO, the lead time to add capacity (autoscaling, quota increase, new region), and the utilisation at which
a capacity ticket opens and at which the capacity owner is paged. Take every number from your own load tests
and procurement lead times.

## Monitoring
Export per-unit utilisation and capacity as metrics, compute the lose-k-largest-units check in a script from
per-cluster capacity, and alert before utilisation exceeds the target.

## Gotchas
- Autoscaling does not remove the need for headroom: the Workbook (Managing Load) recommends user-facing services reserve enough spare capacity for both overload protection and redundancy, and that autoscalers keep the service far from key bottlenecks such as CPU.
- Shared clusters: headroom counted per service vanishes if neighbours spike; reserve or prioritise.
- The book notes capacity plans are a never-ending cycle (Software Engineering in SRE): revise as assumptions change.

## Verify
- [ ] Target derived and documented with inputs.
- [ ] Drill or load test confirms SLO met with the planned number of units removed at peak.
- [ ] Alerts fire before utilisation exceeds the target.

## Checked

2026-11-01. Confirmed against the SRE Book chapters Addressing Cascading Failures (capacity planning coupled with
performance testing; the 5,000 QPS, 19,000 QPS, six-cluster N + 2 example) and Software Engineering in SRE
(capacity planning is a never-ending cycle) and the Workbook chapter Managing Load (spare capacity for overload protection and redundancy). The formulas and the 63% figure are arithmetic on that example.
Removed: the latency-knee, burst factor and 43% example, the policy figures, the PromQL query, the memory-headroom
claim and the Workbook Managing Load claim that sat unread.
Method: documentation only; no commands were run.
