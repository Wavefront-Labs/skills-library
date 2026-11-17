---
id: computing-software.qa-testing-engineering.performance-testing.spike-test-autoscaling
name: spike-test-autoscaling
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [autoscaling-test, spike-testing, scale-out-verification, hpa-load-test]
level: practitioner
status: docs-checked
description: "Design spike tests that verify autoscaling: sudden ramp profiles, measuring scale-out lag, cold starts, queue build-up, recovery after the spike and HPA/ASG metrics to watch."
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/spike-testing/
  - https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spike test design and autoscaling verification

**Question answered:** when traffic jumps suddenly (campaign email, TV ad, retry storm), does the system survive, how long until it scales, and does it recover?

## Profile
```js
scenarios: {
  spike: {
    executor: 'ramping-arrival-rate', startRate: 50, timeUnit: '1s', preAllocatedVUs: 200, maxVUs: 2000,
    stages: [
      { target: 50, duration: '5m' },     // baseline, autoscaler settled
      { target: 1000, duration: '30s' },  // spike
      { target: 1000, duration: '10m' },  // hold: does scale-out catch up?
      { target: 50, duration: '30s' },    // drop
      { target: 50, duration: '10m' },    // recovery + scale-in
    ],
  },
},
```

## What to measure
| Metric | Why |
|---|---|
| Time from spike start to new replicas Ready | scale-out lag (metrics window + scheduling + image pull + startup + readiness) |
| Error rate and p95 during the lag window | user impact before capacity arrives |
| Queue depth / pending connections | backlog and drain time |
| Node autoscaler events | whether pods wait for new nodes |
| Downstream dependencies (DB, third parties) | they usually don't autoscale |
| Scale-in behaviour | flapping, dropped connections on termination |

Kubernetes: watch the HPA and cluster events with kubectl, and review the HPA `behavior` field (scale-up and scale-down policies, `stabilizationWindowSeconds`).

## Typical findings
- An HPA reacts only after its metrics window and sync period; spikes shorter than that are absorbed only by headroom.
- Readiness probes too eager send traffic to cold pods (JIT warm-up, caches empty).
- Connection pools at the DB exhaust as replicas multiply.

## Mitigations to test
Minimum replica headroom, predictive/scheduled scaling before known events, queue-based load levelling, rate limiting with graceful 429 responses.

## Gotchas
- Generators themselves must handle the spike (set `preAllocatedVUs` and `maxVUs` high enough to hold the arrival rate).
- Run in an environment with production-like autoscaling limits and quotas.

## Verify
Report includes the timeline: spike start, first errors, replicas ready, latency back within SLO, scale-in complete.

## Checked
2026-10-28. Confirmed in the k6 ramping-arrival-rate executor page: `startRate`, `timeUnit`, `preAllocatedVUs`, `maxVUs`. Confirmed in the Kubernetes HPA page: the `behavior` field and `stabilizationWindowSeconds`. Removed: the 1-3 minute HPA reaction figure, the `dropped_iterations` metric claim, the specific `kubectl` flags and the `behavior.scaleUp` path, none of which were in the fetched pages.
Method: documentation only; no commands were run.
