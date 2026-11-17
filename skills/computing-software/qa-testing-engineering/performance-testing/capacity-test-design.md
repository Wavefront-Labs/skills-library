---
id: computing-software.qa-testing-engineering.performance-testing.capacity-test-design
name: capacity-test-design
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [capacity-test-design, capacity-testing, max-sustainable-throughput, headroom]
level: practitioner
status: draft
description: "Run capacity tests that find the maximum sustainable throughput within SLOs: stepped load, hold periods, identifying the limiting resource and stating capacity with headroom."
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/breakpoint-testing/
  - https://www.brendangregg.com/usemethod.html
  - https://sre.google/sre-book/handling-overload/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity testing

**Question:** what is the highest load the system sustains while meeting SLOs, and which resource limits it? (Breakpoint tests push until failure; capacity tests stop at the SLO boundary and hold.)

## Stepped profile with holds
```js
stages: [
  { target: 100, duration: '3m' }, { target: 100, duration: '7m' },
  { target: 200, duration: '3m' }, { target: 200, duration: '7m' },
  { target: 300, duration: '3m' }, { target: 300, duration: '7m' },
  { target: 400, duration: '3m' }, { target: 400, duration: '7m' },
]
```
(`ramping-arrival-rate`, rate in iterations/s.) Holds let queues, pools and autoscaling settle so each step reflects steady state.

## Per step record
Achieved throughput, p95/p99, error rate, and USE metrics (utilisation, saturation, errors) for CPU, memory, disk, network, DB connections, thread pools, queues.

## Find the limit
Capacity = the highest step where SLOs hold **and** no resource shows growing saturation (queue length rising over the hold). Name the bottleneck: "DB CPU at 85% on step 300; p95 crosses 300 ms at 340/s".

## State capacity usefully
- Sustainable: 320 req/s at p95 < 300 ms with 4 app replicas, db.r6g.xlarge.
- Planning: with 30% headroom, supports 245 req/s of real traffic; current peak 180 req/s -> 36% growth room.
- Scaling factor: test at 2 and 4 replicas to see whether capacity scales linearly or the DB caps it.

## Gotchas
- Generators must not be the bottleneck (check their CPU and `dropped_iterations`).
- Capacity is specific to data volume, cache hit ratio and mix: document them.
- Results from a smaller environment don't scale linearly to production; state the environment.

## Verify
Repeat the last passing and first failing steps: results reproduce within normal variance.
