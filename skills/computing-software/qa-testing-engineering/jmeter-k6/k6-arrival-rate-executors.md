---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-arrival-rate-executors
name: k6-arrival-rate-executors
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [constant-arrival-rate, ramping-arrival-rate, open-model, k6-executors, throughput-testing]
level: practitioner
status: verified
description: "Model open workloads in k6 with constant-arrival-rate and ramping-arrival-rate: rate and timeUnit, preAllocatedVUs and maxVUs sizing, and why throughput stays fixed."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-arrival-rate/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# constant-arrival-rate and ramping-arrival-rate (k6)

**Goal:** drive a target throughput (iterations per second) regardless of how slow the system gets: an open model, like real internet traffic.

## constant-arrival-rate
```js
export const options = {
  scenarios: {
    checkout: {
      executor: 'constant-arrival-rate',
      rate: 50, timeUnit: '1s',          // 50 iterations started per second
      duration: '20m',
      preAllocatedVUs: 100,               // VUs initialised before start
      maxVUs: 400,                        // k6 may add VUs up to this if iterations take longer (default if unset: same as preAllocatedVUs)
    },
  },
};
```

## ramping-arrival-rate
```js
checkout: {
  executor: 'ramping-arrival-rate',
  startRate: 10, timeUnit: '1s',
  preAllocatedVUs: 50, maxVUs: 500,
  stages: [
    { target: 50, duration: '5m' },      // ramp to 50 it/s
    { target: 50, duration: '20m' },     // hold
    { target: 150, duration: '10m' },    // push to 150 it/s
    { target: 0, duration: '2m' },
  ],
},
```

## Sizing VUs (Little's law)
VUs needed = rate x iteration duration (seconds). 50 it/s x 1.2 s per iteration (incl. sleeps) = 60 VUs; allocate headroom for slowdowns: `preAllocatedVUs` ~ 1.5-2x (a rule of thumb, not from the docs), `maxVUs` for degraded response times.
Run check (k6 2.3.0, 50 it/s against an endpoint taking 0.4 s, 6 s run): `vus` peaked at 20 = 50 x 0.4. With `preAllocatedVUs: 5, maxVUs: 40` the run still dropped 16 iterations because VUs were being initialised mid-test (the docs warn that a low `preAllocatedVUs` costs rate); with `maxVUs: 10` it dropped 155 and logged `Insufficient VUs, reached 10 active VUs and cannot initialize more`.

## Open vs closed
- Open (arrival-rate): iterations keep starting at the configured rate however slow the system is, so the system sees queueing and latency growth as in real overload. k6 itself never queues: once no VU is free, scheduled iterations are dropped and counted in `dropped_iterations`.
- Closed (`constant-vus`, `ramping-vus`): each VU waits for its response, so a slow system receives less load (coordinated omission). Use for "N concurrent users" questions.

## Rules
- Do not add `sleep` to pace iterations in arrival-rate executors; the executor already paces. Think time inside a multi-step iteration is fine but increases VU need.
- Watch `dropped_iterations`: if > 0, maxVUs was too small or the load generator is saturated, so the target rate was not achieved.

## Verify
`iterations` rate in the summary equals the target, `dropped_iterations` is zero (or explained), and latency is reported at the intended throughput.
