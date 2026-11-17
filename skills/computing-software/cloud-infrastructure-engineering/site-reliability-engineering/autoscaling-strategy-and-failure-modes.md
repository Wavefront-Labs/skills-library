---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.autoscaling-strategy-and-failure-modes
name: autoscaling-strategy-and-failure-modes
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [autoscaling-strategy, autoscaling-with-load-balancing, hpa, handling-overload, managing-load, scale-down-protection]
level: advanced
status: docs-checked
description: "Design autoscaling that helps instead of hurts: signals, min/max bounds, unhealthy-instance traps, dependency failures and interaction with load balancing, from the SRE Workbook."
sources: ["https://sre.google/workbook/managing-load/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscaling strategy and failure modes

Workbook "Managing Load" lists autoscaling best practices and failure modes.

## Failure modes and mitigations (Workbook)
| Failure mode | Mitigation |
|---|---|
| Unhealthy (non-serving) instances still count toward the utilisation average, so autoscaling simply does not occur | autoscale on a capacity metric observed by the load balancer, which discounts unhealthy instances; use autohealing and leave time for restarted instances to become healthy |
| A bug makes servers burn CPU without doing work; a CPU-based autoscaler upsizes again and again until quota is wasted | set a minimum and maximum bound for scaling, with enough quota for the limits |
| A dependency is failing, requests get stuck, and scaling up adds traffic to the failing dependency | the book notes the added load can stop the dependency recovering; bound the maximum size |
| Scaling down too eagerly | the book says scaling up matters more and is less risky than scaling down; autoscalers wait longer before reducing resources |
| New instances cannot serve instantly | keep spare capacity: the book recommends user-facing services reserve enough for both overload protection and redundancy |

## Design rules from the Workbook
- Configure the autoscaler to keep the service far from key bottlenecks such as CPU; the load spikes you can
  absorb grow as you move away from a bottleneck.
- Constrain the autoscaler with minimum and maximum bounds, and make sure quota covers the limits; this also
  helps capacity planning.
- Autoscaling normally averages utilisation across instances and assumes they are homogeneous in efficiency.
- Complex systems may need both load balancing and load-based autoscaling: for example several managed instance
  groups cloned across regions need traffic balanced between regions.
- Keep load shedding as well: an autoscaler needs time to react.

## Kubernetes
For Horizontal Pod Autoscaler behaviour (metrics, stabilization windows, scaling policies) read the Kubernetes
documentation for your version before relying on field names; this skill does not restate them.

## Verify
- [ ] Load test: step increase reaches new steady state within SLO.
- [ ] Simulated unhealthy instances do not cause the autoscaler to mis-scale.

## Checked

2026-11-01. Confirmed against the SRE Workbook chapter Managing Load (unhealthy instances and the average,
load-balancer capacity metric, autohealing, CPU-bug and failing-dependency examples, min and max bounds with quota,
scale up versus scale down, spare capacity for overload protection and redundancy, load balancing plus autoscaling).
Removed: the HPA manifest and its figures, the monitoring metric names and alert time, the CPU 70% claim, the
memory-HPA and VPA claims and the slow-start row (none stated on the page read).
Method: documentation only; no commands were run.
