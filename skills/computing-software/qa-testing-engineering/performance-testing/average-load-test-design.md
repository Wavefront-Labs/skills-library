---
id: computing-software.qa-testing-engineering.performance-testing.average-load-test-design
name: average-load-test-design
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [average-load-test, load-test-design, steady-state, baseline-load]
level: practitioner
status: verified
description: "Design an average-load test: derive typical-day traffic, ramp-up, steady-state duration, pass criteria from SLOs, and keep the profile comparable across releases."
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/load-testing/
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Average-load test design

**Purpose:** prove the system meets SLOs under normal expected traffic, and produce a baseline to compare releases against.

## Inputs
- Typical busy-hour throughput from production (requests/s per endpoint or journeys/hour), not the yearly peak.
- Transaction mix (from analytics/access logs).
- SLOs: e.g. p95 < 300 ms for reads, error rate < 0.5%.

## Profile
```js
export const options = {
  scenarios: {
    average: {
      executor: 'ramping-arrival-rate', startRate: 0, timeUnit: '1s',
      preAllocatedVUs: 100, maxVUs: 300,
      stages: [
        { target: 120, duration: '5m' },   // ramp-up (k6's own example: 5 min ramp, 30 min hold, 5 min ramp-down)
        { target: 120, duration: '30m' },  // steady state
        { target: 0, duration: '5m' },     // ramp-down
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.005'],
    'http_req_duration{type:read}': ['p(95)<300'],
    'http_req_duration{type:write}': ['p(95)<600'],
  },
};
```
Arrival-rate (open model) keeps request rate constant even if the system slows, which is how real traffic behaves. The threshold keys `'http_req_duration{type:read}'` only match requests that carry a `type` tag, so set it per request, for example `http.get(url, { tags: { type: 'read' } })`; a scaled-down copy of this profile (20/s, 2 s up, 4 s hold, 2 s down, requests tagged read and write) passed all three thresholds with exit code 0 and reported each tagged sub-metric separately.

## Duration
Steady state long enough to see caches warm, GC cycles, connection pool behaviour: 30-60 minutes is a common rule of thumb (k6's example holds for 30 minutes); shorter runs only for smoke.

## Evaluate
- Thresholds on steady-state window (exclude ramp).
- Server-side: CPU with headroom (a common rule of thumb is below ~70%), no growing queues, DB connection pool not exhausted.
- Compare against the previous release's run: same profile, same data size, same environment.

## Gotchas
- "Average" from daily totals / 86,400 is far below busy-hour reality; use the busiest normal hour.
- Changing the script or environment between runs breaks comparability; version the profile.
- Load from one region only misses latency other users see; note it as a limitation.

## Verify
Two consecutive runs on the same build give p95 within a few percent (aim for the 5-10% rule of thumb): the baseline is stable enough to detect regressions.

## Checked
k6 v1.4.0 on Windows against a local stdlib HTTP server; fetched docs.
- Run: the `ramping-arrival-rate` profile with `startRate: 0` and the three thresholds, durations scaled from 5/30/5 min to 2/4/2 s, with `{ tags: { type: 'read' } }` and `{ type: 'write' }` on the requests: all thresholds passed (p95 0.68 ms and 0.74 ms, failure rate 0%).
- Fetched: k6 load-testing guide and test-types page (average-load purpose, ramp/steady/ramp-down shape), k6 scenarios page.
- k6's average-load page uses 5 min ramp-up, 30 min hold and 5 min ramp-down, which the profile mirrors; the other durations and percentages in the body are labelled as rules of thumb.
