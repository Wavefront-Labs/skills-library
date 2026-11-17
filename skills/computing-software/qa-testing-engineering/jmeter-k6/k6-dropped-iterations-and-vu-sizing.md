---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-dropped-iterations-and-vu-sizing
name: k6-dropped-iterations-and-vu-sizing
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [dropped-iterations, k6, preallocatedvus, arrival-rate, load-generator-capacity]
level: practitioner
status: verified
description: "Diagnose k6 dropped_iterations: insufficient preAllocatedVUs or maxVUs, slow responses, load generator saturation, and how to size VUs and read the warning."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/
  - https://grafana.com/docs/k6/latest/testing-guides/running-large-tests/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dropped iterations and preAllocatedVUs sizing (k6)

**Symptom:** `dropped_iterations` metric > 0 and the warning "Insufficient VUs, reached N active VUs and cannot initialize more". The target arrival rate was not achieved, so the test did not apply the load you think.

## Causes
1. **VU pool too small**: `preAllocatedVUs`/`maxVUs` below rate x iteration duration.
2. **System slowed down**: iteration duration grew (latency rising), needing more VUs than allowed. This is a finding about the system, not only a config error.
3. **Load generator saturated**: CPU at 100%, k6 cannot start iterations on time.
4. **Iteration cap executors**: with `shared-iterations` and `per-vu-iterations`, iterations drop if `maxDuration` is reached before all finish (raise the duration).

## Sizing
```
VUs = target rate (it/s) x p95 iteration duration (s) x safety factor (1.5-2)
e.g. 100 it/s x 1.5 s x 1.5 = 225 preAllocatedVUs; maxVUs 400 for degradation
```
Measure iteration duration with the built-in `iteration_duration` trend from a smoke run.
Pre-allocating is better than relying on `maxVUs`: initialising VUs mid-test costs CPU and adds latency on the generator.

## Diagnose
- Compare `iterations` rate vs configured rate over time (Grafana output, `--out json`).
- Plot `vus` against `http_req_duration`: VUs climbing to `maxVUs` as latency rises = system saturation.
- Check generator CPU/memory/network (see load-generator saturation skill); fewer checks, tags and output points reduce CPU. `--compatibility-mode=base` does not help: since k6 0.53 the mode only changes the `global` alias (k6 docs).

## Actions
- Config cause: raise preAllocatedVUs/maxVUs, then rerun.
- System cause: report the throughput at which latency degraded; that is the capacity knee.
- Generator cause: distribute across more machines (k6 operator, Grafana Cloud k6) or optimise the script.

## Thresholds
Make it a gate so silent under-load fails the run:
```js
thresholds: { dropped_iterations: ['count<10'] }
```
Run (k6 2.3.0, 50 it/s of 0.4 s requests with `maxVUs: 5`): `dropped_iterations count=150`, threshold marked failed, exit code 99.

## Verify
Rerun shows zero (or explained) dropped iterations, achieved rate equals target, and the generator stays under about 80% CPU (the k6 large-tests guide recommends at least 20% idle CPU).
