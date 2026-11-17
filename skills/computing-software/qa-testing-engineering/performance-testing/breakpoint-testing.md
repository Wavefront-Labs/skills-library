---
id: computing-software.qa-testing-engineering.performance-testing.breakpoint-testing
name: breakpoint-testing
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [breakpoint-testing, capacity-testing, stress-testing, ramping-arrival-rate, saturation-point]
level: practitioner
status: verified
description: "Find a system's capacity limit with a breakpoint test: slowly ramp arrival rate until SLOs break or errors climb, abort safely, and locate the saturating resource."
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/breakpoint-testing/
  - https://www.brendangregg.com/usemethod.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Breakpoint testing to find the limit

**Goal:** know the throughput at which the system stops meeting its objectives, and which resource limits it.

## Design
- Open model (arrival rate) so load keeps increasing even as latency rises.
- Slow continuous ramp or small steps (each step long enough to stabilise, e.g. 5 min).
- Stop conditions: SLO breach, error rate above a safety limit, or generator saturation.
```js
export const options = {
  scenarios: {
    breakpoint: {
      executor: 'ramping-arrival-rate',
      startRate: 20, timeUnit: '1s',
      preAllocatedVUs: 200, maxVUs: 3000,
      stages: [{ target: 2000, duration: '2h' }],      // keep ramping until something breaks
    },
  },
  thresholds: {
    http_req_failed: [{ threshold: 'rate<0.05', abortOnFail: true, delayAbortEval: '1m' }],
    http_req_duration: [{ threshold: 'p(95)<2000', abortOnFail: true, delayAbortEval: '1m' }],
  },
};
```

A scaled-down copy of this config (stage target 2000 over 30 s, thresholds `p(95)<0.3` ms to force a breach, `delayAbortEval: '3s'`) stopped after about 4 s with `thresholds on metrics 'http_req_duration' were crossed; at least one has abortOnFail enabled, stopping test prematurely` and exit code 99. With realistic limits against a fast local server nothing breached and the ramp ran to 1,000 requests/s. The k6 docs say to stop a breakpoint test manually (Ctrl+C) or with a threshold that has `abortOnFail: true`.

## Environment
Production-like sizing and data; autoscaling either disabled (find per-instance limit) or enabled with max replicas known (find system limit). Notify owners of shared dependencies.

## Analysis
1. Plot throughput achieved vs offered, latency percentiles, errors over time.
2. **Knee point**: where latency starts rising non-linearly; **breakpoint**: where errors or SLO breaches begin.
3. At the knee, find the saturated resource using the USE method (CPU, memory, connection pools, DB locks, thread pools, network) via APM and server metrics.
4. Report: capacity = highest throughput meeting SLO, the bottleneck, and headroom vs peak production load (e.g. limit 850 RPS vs peak 400 = 2.1x, computed as 850 / 400 = 2.125).

## Gotchas
- Generator saturation looks like a system limit; check generator CPU and `dropped_iterations`.
- Caches warm during the ramp; long ramps change the system state (data growth) too.
- Never run against production without an explicit plan and approval.

## Verify
The report names the capacity number, the limiting resource with evidence, and the safety stop that ended the test.

## Checked
k6 v1.4.0 on Windows against a local stdlib HTTP server; fetched docs.
- Run: the breakpoint scenario (`ramping-arrival-rate`, `startRate`, `preAllocatedVUs`, `maxVUs`, one 30 s stage in place of 2 h) with the two `abortOnFail`/`delayAbortEval` thresholds: no abort when limits were loose (30,298 iterations), abort with exit code 99 when the p95 limit was set to 0.3 ms.
- Fetched: k6 breakpoint-testing guide (open model via `ramping-arrival-rate` "assure load increase if the system slows", stop manually or with `abortOnFail`), Brendan Gregg's USE method page (URL live).
- Computed: 850 / 400 = 2.125.
