---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-graceful-stop-and-ramp-down
name: k6-graceful-stop-and-ramp-down
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [gracefulstop, gracefulrampdown, interrupted-iterations, k6-scenarios]
level: practitioner
status: verified
description: "Configure k6 gracefulStop and gracefulRampDown so in-flight iterations finish cleanly at scenario end or ramp-down, and read interrupted iteration counts."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/graceful-stop/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gracefulStop and gracefulRampDown

## gracefulStop (all executors)
When a scenario's duration ends, running iterations get `gracefulStop` time (default **30s**) to finish before being interrupted.
```js
scenarios: {
  checkout: {
    executor: 'constant-vus', vus: 50, duration: '10m',
    gracefulStop: '2m',        // long multi-step journeys
  },
},
```
Total scenario time = duration + up to gracefulStop.

## gracefulRampDown (ramping-vus)
When stages reduce VUs, VUs being removed may finish their current iteration within `gracefulRampDown` (default 30s):
```js
{ executor: 'ramping-vus', stages: [{ duration: '5m', target: 100 }, { duration: '2m', target: 0 }], gracefulRampDown: '1m' }
```
Set `gracefulRampDown: '0s'` to drop VUs immediately (sharper load profile, more interrupted iterations). Run: 2 VUs ramped to 0 over 1 s with 1.5 s requests gave 2 complete and 2 interrupted iterations at `0s`, and 4 complete and 0 interrupted at the default 30 s.

## Interrupted iterations
The progress line (`running (3.0s), 0/1 VUs, 1 complete and 1 interrupted iterations`) reports the count; the end-of-test `iterations` metric counts only completed ones. Interrupted iterations don't emit metrics for unfinished requests: with `gracefulStop: '0s'` and 2 s requests in a 3 s run, `http_reqs` was 1 although a second request was in flight; with `gracefulStop: '5s'` it was 2 (k6 2.3.0). Many interruptions:
- Iteration longer than gracefulStop (raise it, or shorten journeys).
- Long `sleep()` at the end of iterations: k6 interrupts sleeping VUs too (run: `sleep(10)` after each request with `gracefulStop: '0s'` ended the run at 3 s, one interrupted iteration).

## Chaining with startTime
Next scenario's `startTime` should account for the previous scenario's duration **plus** gracefulStop if they must not overlap.

## teardown
`teardown()` runs after all scenarios finish (including graceful periods), with `teardownTimeout` (default 60s, as is `setupTimeout`; k6 options reference).

## Gotchas
- Thresholds evaluate over the whole run including graceful periods.
- Arrival-rate executors also honour gracefulStop; no new iterations start after duration (run: `constant-arrival-rate` 5/s for 3 s with 2 s requests and `gracefulStop: '5s'` completed 15 iterations, all finishing by 4.8 s, none interrupted).

## Verify
End summary reports zero (or explained) interrupted iterations; scenario timeline in outputs matches planned duration plus grace.
