---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-externally-controlled-executor
name: k6-externally-controlled-executor
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [externally-controlled, k6-rest-api, k6-scale, live-load-control]
level: practitioner
status: verified
description: "Change k6 load during a run with the externally-controlled executor and k6's REST API or k6 scale/pause/resume commands, for exploratory capacity probing."
sources:
  - https://github.com/grafana/k6/releases/tag/v2.0.0
  - https://grafana.com/docs/k6/latest/reference/k6-rest-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# externally-controlled executor and the k6 REST API

**REMOVED in k6 v2.0.0.** The `externally-controlled` executor, `k6 scale`, `k6 pause`, `k6 resume` and `k6 status` no longer exist (v2.0.0 release notes: no replacement). Run on k6 2.3.0 the script below fails at start with `unknown executor type 'externally-controlled'`. The technique works only on k6 1.x (everything below was run on 1.8.2). On v2 use stepped `ramping-vus` or `ramping-arrival-rate` stages and re-run, or watch a dashboard while a long ramp executes.

**Use (k6 1.x):** exploratory sessions where you raise or lower VUs live while watching dashboards, instead of re-running with new stages.

```js
export const options = {
  scenarios: {
    probe: { executor: 'externally-controlled', vus: 10, maxVUs: 500, duration: '1h' },
  },
};
```
It supports VU-based control (not arrival rate). Older docs say it must be the only scenario, but on 1.8.2 a script with this scenario plus a `constant-vus` one ran normally.

## Controlling it
On k6 1.x the REST API listens on `localhost:6565` by default (`--address` to change; run on 1.8.2). From v2 the API server no longer starts unless you pass `--address`.
```bash
k6 scale --vus 100            # change active VUs (<= maxVUs)
k6 scale --max 800            # raise the cap
k6 pause / k6 resume
k6 status                     # running state, VUs, iterations
k6 stats                      # current metrics
curl -X PATCH localhost:6565/v1/status -H 'Content-Type: application/json' \
  -d '{"data":{"type":"status","id":"default","attributes":{"vus":150}}}'
```
Start paused: `k6 run --paused script.js`, then `k6 resume` (run on 1.8.2: `k6 status` showed `paused: "true"`, `vus: "0"`, then 2 VUs after resume). Run results on 1.8.2: `k6 scale --vus 8` took `vus` from 2 to 8; the `PATCH /v1/status` call with `vus: 12` returned `"vus":12`; `k6 pause` set `vus: "0"` and `k6 resume` restored 12.

## Probing method
1. Start at a safe baseline; let metrics settle (2-5 min).
2. Step up (e.g. +25%) and hold; note p95 latency, error rate, server CPU/DB.
3. Stop when SLO breaks; record the last good level.
4. Turn findings into a scripted `ramping-vus` or `ramping-arrival-rate` test so it's repeatable.

## Gotchas
- Results mix many load levels: tag time windows in notes, or rely on time-series outputs, not the end summary.
- Closed model: raising VUs on a slowing system doesn't raise throughput proportionally.

## Verify
`k6 status` reflects the new VU count and the time-series dashboard shows the step.
