---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-vu-based-executors
name: k6-vu-based-executors
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [ramping-vus, constant-vus, per-vu-iterations, shared-iterations, k6-executors]
level: practitioner
status: verified
description: "Choose k6 VU-based executors: constant-vus, ramping-vus stages, per-vu-iterations and shared-iterations, gracefulStop and gracefulRampDown, and closed-model caveats."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-vus/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/graceful-stop/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ramping-vus, constant-vus and per-vu-iterations (k6)

## Executors
| Executor | Behaviour | Use for |
|---|---|---|
| `constant-vus` | N VUs loop for a duration | steady concurrent users, soak |
| `ramping-vus` | VUs follow stages | classic ramp-up/hold/ramp-down load, spike |
| `per-vu-iterations` | each VU runs exactly N iterations | fixed work per user (each user processes its own data) |
| `shared-iterations` | N iterations total shared across VUs | "process 10,000 items as fast as possible", data migration checks |
| `externally-controlled` | VUs changed at runtime via REST API/CLI (removed in k6 v2.0.0; k6 1.x only) | manual exploratory load |

## Examples
```js
export const options = {
  scenarios: {
    shoppers: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 200 },
        { duration: '30m', target: 200 },
        { duration: '5m', target: 0 },
      ],
      gracefulRampDown: '30s',     // let iterations finish when VUs are removed
      gracefulStop: '30s',         // at scenario end
    },
    importers: {
      executor: 'per-vu-iterations',
      vus: 10, iterations: 50, maxDuration: '15m',
      exec: 'importFile',
    },
  },
};
```
The `stages` shortcut at top level (`options.stages`) creates a ramping-vus scenario named `default` (run: `* default: Up to 2 looping VUs for 2s over 2 stages (gracefulRampDown: 30s, gracefulStop: 30s)`). The example above ran on k6 2.3.0 and printed `importers: 4 iterations for each of 3 VUs` (scaled down) with the default `maxDuration`/`gracefulStop` shown.

## Closed-model caveats
- Throughput = VUs / (response time + think time). As the system slows, throughput drops, hiding overload (coordinated omission). Report achieved RPS, not just VUs.
- Add realistic `sleep()` think time; zero sleep with VUs measures maximum throughput per VU, not users.

## Graceful stop
Iterations still running at the end are allowed `gracefulStop` (default 30 s) to finish; then interrupted. Interrupted iterations are reported in the progress line (`N complete and M interrupted iterations`) and are not counted as failures or in the `iterations` metric. Long iterations need longer grace (see the gracefulStop skill for the run).

## Gotchas
- `shared-iterations` gives uneven work per VU; fast VUs do more (run: 40 iterations over 2 VUs split 36 and 4 when one VU's requests were 10x faster).
- Stages with sudden jumps create spikes in connection setup; ramp gradually unless spike testing.

## Verify
Achieved RPS and VU curves match intent in the output, and interrupted iterations at stop are near zero.
