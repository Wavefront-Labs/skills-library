---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.stress-tests-and-breaking-points
name: stress-tests-and-breaking-points
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [stress-tests, breaking-point-testing, testing-for-reliability, load-testing, k6, failure-modes]
level: practitioner
status: docs-checked
description: "Run stress tests past capacity to find breaking points and how the system fails: graceful degradation or collapse, recovery after load drops, and which resource gives out first."
sources: ["https://sre.google/sre-book/testing-reliability/", "https://sre.google/sre-book/addressing-cascading-failures/", "https://grafana.com/docs/k6/latest/testing-guides/test-types/stress-testing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stress tests and breaking points

SRE Book: stress tests answer "how full can a database get before writes start to fail?" and "at how many
QPS does an application server become unavailable?". Capacity tests find the safe operating point; stress
tests find what happens beyond it.

## Questions to answer
1. At what load does each SLI break (latency first, then errors)?
2. Which resource saturates first (CPU, memory, connections, threads, file descriptors, DB pool, downstream)?
3. Does the system degrade gracefully (rejects excess with 429/503, keeps serving the rest) or collapse
   (throughput drops toward zero, crash loops)?
4. Does it **recover** by itself when load returns to normal, and how long does it take?

## Test shape
```javascript
// k6 stages shape: ramp above average load, hold, then drop back (add a recovery stage at normal load)
export const options = {
  stages: [
    { duration: '10m', target: 200 }, // ramp up to a higher load
    { duration: '30m', target: 200 }, // hold it
    { duration: '5m', target: 0 },    // ramp down; then check recovery at normal load
  ],
};
```
Watch goodput (successful responses/s), not just throughput. A good system's goodput plateaus at capacity;
a bad one's falls.

## What to record
- Load at first SLO breach, at 1% errors, at collapse.
- Resource graphs at each point; the first saturated resource is the next optimisation target.
- Recovery time after load drops; if it never recovers, you have a cascading-failure risk
  (see `cascading-failure-testing`).

## Datastores
- Fill tests: write until disk/quota full in a test environment; confirm alerts fire before failure and
  the failure mode (read-only? crash? corruption?).
- Connection storms: open connections to max_connections and beyond.

## Gotchas
- Run against an isolated environment sized like prod, or a carefully bounded production slice with
  abort criteria.
- Client timeouts in the load generator must match real clients, or retries/timeouts behave differently.
- Autoscaling hides breaking points; test with it on and off.

## Verify
- [ ] Breaking point and failure mode documented per service.
- [ ] Load shedding engages before collapse; recovery is automatic within a stated time.

## Checked
2026-11-01. Confirmed in the SRE Book Testing for Reliability (stress tests find the limits of a service and its components, which often fail catastrophically rather than degrade gracefully) and the k6 stress-testing page (load above average, longer ramp, run after average-load tests, reuse the average-load script, expect worse performance, stages option). Replaced the arrival-rate executor example with the page's stages shape. Goodput and datastore fill tests are practice advice, not sourced claims.
Method: documentation only; no commands were run.
