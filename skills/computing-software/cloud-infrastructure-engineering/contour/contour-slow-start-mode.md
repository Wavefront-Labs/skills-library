---
id: computing-software.cloud-infrastructure-engineering.contour.contour-slow-start-mode
name: contour-slow-start-mode
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [slowstartpolicy, slow-start, jvm, warm-up, window, aggression, minweightpercent]
level: practitioner
status: docs-checked
description: "HTTPProxy slowStartPolicy to ramp traffic to new endpoints: window, aggression easing, minWeightPercent, supported strategies, JVM warm-up use case."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/slow-start.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Slow start mode

Slow start gradually increases traffic to a newly added upstream endpoint, which helps JVM apps that struggle during JIT warm-up or right after a container restart.

```yaml
routes:
- services:
  - name: java-app
    port: 80
    slowStartPolicy:
      window: 3s
      aggression: "1.0"
      minWeightPercent: 10
```

- `window`: duration of the ramp. By default traffic rises linearly from 10% of the target load balancing weight to 100% across it.
- `aggression` (optional): easing function of the increase, written as a quoted string in the example. Above 1.0 ramps fast first and slows near the end of the window; below 1.0 starts slowly and speeds up near the end.
- `minWeightPercent` (optional): minimum percentage of target weight, avoiding such tiny initial weights that the endpoint gets no traffic at the start of the window.

The setting is on a service entry under a route, as in the example. It works only with the `RoundRobin` and `WeightedLeastRequest` load balancing strategies. See the Envoy slow start documentation for details.

## Checked

2026-11-08. Read the Contour main-branch config page slow-start.md in full. Confirmed: purpose and JVM use case, default linear ramp from 10%, `window`, `aggression` direction semantics, `minWeightPercent`, the example placement, and the RoundRobin and WeightedLeastRequest restriction. Removed the claim that other strategies ignore the setting and the advice on sizing the window and readiness probes, which the page does not state.

Method: documentation only; no commands were run.
