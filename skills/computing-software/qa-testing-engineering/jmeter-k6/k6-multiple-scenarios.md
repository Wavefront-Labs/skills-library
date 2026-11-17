---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-multiple-scenarios
name: k6-multiple-scenarios
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-multiple-scenarios, k6-scenarios, k6-executors, mixed-workload, exec-function]
level: practitioner
status: verified
description: "Combine multiple k6 scenarios in one test: per-scenario exec functions, executors and env, startTime offsets, tags, and thresholds per scenario for mixed workloads."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/advanced-examples/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple concurrent scenarios with exec functions (k6)

**Goal:** a realistic mix (browsers, buyers, API clients, background jobs) running together with different load shapes.

## Example
```js
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  scenarios: {
    browse: {
      executor: 'ramping-vus', exec: 'browse',
      stages: [{ duration: '5m', target: 300 }, { duration: '30m', target: 300 }],
      tags: { flow: 'browse' },
    },
    buy: {
      executor: 'constant-arrival-rate', exec: 'buy',
      rate: 8, timeUnit: '1s', duration: '30m', startTime: '5m',      // starts after browse ramp
      preAllocatedVUs: 40, maxVUs: 150,
      tags: { flow: 'buy' },
    },
    partner_api: {
      executor: 'constant-arrival-rate', exec: 'partnerSync',
      rate: 120, timeUnit: '1m', duration: '35m', preAllocatedVUs: 5,
      env: { CLIENT: 'partner-a' },
    },
    nightly_report: {
      executor: 'shared-iterations', exec: 'report', vus: 1, iterations: 1, startTime: '20m',
    },
  },
  thresholds: {
    'http_req_duration{scenario:buy}': ['p(95)<800'],
    'http_req_duration{scenario:browse}': ['p(95)<400'],
    'http_req_failed{scenario:partner_api}': ['rate<0.001'],
  },
};

export function browse() { http.get(`${__ENV.BASE_URL}/`); sleep(Math.random() * 5 + 2); }
export function buy() { /* basket + checkout */ }
export function partnerSync() { http.get(`${__ENV.BASE_URL}/api/partner/orders?client=${__ENV.CLIENT}`); }
export function report() { http.post(`${__ENV.BASE_URL}/api/reports/run`); }
```

## Rules
- Each scenario has its own executor, VUs, `exec`, `env`, `tags`, `startTime`, `gracefulStop`.
- The `scenario` system tag is added automatically; thresholds per scenario use `{scenario:name}`.
- Derive the mix from production analytics (ratio of flows per hour); see workload modelling.
- `exec.scenario.name` (k6/execution) inside code if one function serves several scenarios.
- Run check (k6 2.3.0, the example scaled to seconds): `setup()` ran once for four scenarios, `partnerSync` saw `__ENV.CLIENT === 'partner-a'` and `exec.scenario.name === 'partner_api'`, `report` started at 4 s (`startTime`), and the per-scenario thresholds `{scenario:buy}`, `{scenario:browse}`, `{scenario:partner_api}` and the custom-tag `{flow:buy}` all evaluated and passed. `--summary-mode=full` prints a per-scenario breakdown with its own `http_reqs`.

## Gotchas
- `setup()` is shared by all scenarios; there is no per-scenario setup (branch on data in setup instead).
- Total VUs across scenarios count against load generator capacity; check CPU.

## Verify
Per-scenario request rates in results match the modelled mix, and each scenario has its own thresholds.
