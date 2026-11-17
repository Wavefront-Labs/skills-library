---
id: computing-software.qa-testing-engineering.performance-testing.cache-warmup-and-ramp-design
name: cache-warmup-and-ramp-design
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [cache-warmup, ramp-up-design, jit-warmup, cold-start-measurement]
level: practitioner
status: verified
description: "Design warm-up and ramp phases for performance tests: JIT/cache/pool warm-up, excluding warm-up from results, ramp rate choice, and measuring cold-start behaviour deliberately."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/
  - https://grafana.com/docs/k6/latest/using-k6/tags-and-groups/
  - https://jmeter.apache.org/usermanual/generating-dashboard.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache warm-up and ramp design

## Why warm up
Right after deploy: empty caches (app, CDN, DB buffer pool), JIT not compiled (JVM, .NET), connection pools not filled, autoscaled pods cold. The first minutes measure startup, not steady-state capacity.

## Pattern
1. **Warm-up phase:** low-to-moderate load for a few minutes (a rule of thumb: size it by how long caches and pools take to fill) covering the main code paths and a representative data spread.
2. **Ramp:** to target at a rate production could plausibly see (and slow enough to observe where degradation begins).
3. **Steady state:** the measured window.
4. Exclude warm-up/ramp from pass/fail.

k6 (the `scenarios` and `thresholds` keys go inside `export const options = { ... }`; the scenario `tags` become `phase` tags on every request, so the threshold below selects only the main phase):
```js
scenarios: {
  warmup: { executor: 'constant-arrival-rate', rate: 20, timeUnit: '1s', duration: '5m', preAllocatedVUs: 30, tags: { phase: 'warmup' } },
  main: { executor: 'ramping-arrival-rate', startTime: '5m', startRate: 20, timeUnit: '1s', preAllocatedVUs: 200,
          stages: [{ target: 200, duration: '10m' }, { target: 200, duration: '30m' }], tags: { phase: 'main' } },
},
thresholds: { 'http_req_duration{phase:main}': ['p(95)<300'] },
```
JMeter: separate setUp-like Thread Group or `jmeter.reportgenerator.start_date` (all report-generator properties carry the `jmeter.reportgenerator.` prefix; the date format is set by `date_format`) to cut warm-up out of the dashboard. Locust: `--reset-stats` resets statistics once spawning has been completed.
A scaled-down copy of the k6 example (3 s warm-up at 20/s, then a 5 s ramp to 200/s; `startTime: '3s'`) ran with the sub-metric `http_req_duration{phase:main}` reported in its own THRESHOLDS entry, so warm-up requests are excluded from that gate.

## Ramp rate
- Too fast: connection storms and autoscaler lag dominate (that's a spike test).
- Too slow: wastes time; long ramps also mask resource leaks less than soak tests do.
- A rule of thumb (not from a standard): ramp over roughly 10-20% of the total duration.

## Cold-start as its own test
When cold behaviour matters (serverless, scale-to-zero, after deploys), measure it explicitly: restart, then apply load immediately and report first-minute latency separately.

## Gotchas
- Warming only one product id warms one cache entry; warm with the same distribution as the test.
- CDN warm-up from one region doesn't warm other edges.

## Verify
Latency in the first minutes of the main phase is consistent with the rest of the steady state (no downward trend).

## Checked
k6 v1.4.0 on Windows against a local stdlib HTTP server; fetched docs.
- Run: the warm-up plus `ramping-arrival-rate` main scenario with `startTime`, scenario `tags` and the `{phase:main}` threshold, durations scaled down (880 iterations, threshold evaluated on the main phase only, exit code 0).
- Fetched: JMeter dashboard-generation page (`jmeter.reportgenerator.` prefix, `start_date`, `date_format`), Locust configuration page (`--reset-stats` description), k6 scenarios page (executors, `startTime`).
- Durations such as the warm-up length are labelled rules of thumb in the body; the checked parts are the k6 and JMeter mechanics.
