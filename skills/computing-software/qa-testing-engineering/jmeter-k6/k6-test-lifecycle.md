---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-test-lifecycle
name: k6-test-lifecycle
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-lifecycle, k6, setup-teardown, init-context, load-testing]
level: practitioner
status: verified
description: "Use the k6 test lifecycle correctly: init code, setup() and teardown() data passing, VU code iterations, what runs where, and handleSummary at the end."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/test-lifecycle/
  - https://grafana.com/docs/k6/latest/using-k6/test-lifecycle/#setup-and-teardown-stages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k6 test lifecycle (init, setup, VU code, teardown)

## Stages
```js
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

// 1. INIT: runs once per VU, plus extra runs in the VU-0 context (setup/teardown and option gathering). Load files, define options. No HTTP here.
export const options = { vus: 20, duration: '5m' };
const users = new SharedArray('users', () => JSON.parse(open('./users.json')));

// 2. SETUP: runs once before the test. Can make requests. Return value goes to every VU (serialised JSON).
export function setup() {
  const res = http.post(`${__ENV.BASE_URL}/api/test/seed`, JSON.stringify({ products: 100 }),
                        { headers: { 'Content-Type': 'application/json' } });
  return { productIds: res.json('ids'), token: res.json('adminToken') };
}

// 3. VU CODE: default (or scenario exec) function, runs repeatedly per VU = iterations.
export default function (data) {
  const user = users[__VU % users.length];
  const id = data.productIds[Math.floor(Math.random() * data.productIds.length)];
  const res = http.get(`${__ENV.BASE_URL}/api/products/${id}`, { headers: { 'X-User': user.email } });
  check(res, { 'status 200': (r) => r.status === 200 });
}

// 4. TEARDOWN: runs once after all VUs finish (also after an abort during the run; it does NOT run if setup() threw or aborted: run gave exit 107 and no teardown output).
export function teardown(data) {
  http.post(`${__ENV.BASE_URL}/api/test/cleanup`, null, { headers: { Authorization: `Bearer ${data.token}` } });
}

// 5. handleSummary(data): customise end-of-test output (see handlesummary skill).
```

## Rules
- `open()` only in init; file reads in VU code are not allowed.
- Init runs per VU: large JSON parsed per VU multiplies memory; use `SharedArray` (read-only, one copy).
- `setup()` data is serialised to JSON and copied to each VU; functions in it fail (`error marshaling setup() data to JSON`). Changes are local: a VU's edit to `data.n` persisted across that VU's iterations (2, then 3) but `teardown` saw the original (1), and other VUs never see it. Do not rely on mutating it.
- Init-context runs (k6 2.3.0, `vus: 3`): the top-level code printed `vu=0` four times and `vu=1..3` once each; `setup` and `teardown` both reported `__VU === 0`. `__ITER` does not exist in init (`ReferenceError: __ITER is not defined`).
- Setup and teardown have their own timeouts: `setupTimeout`, `teardownTimeout` (default 60 s).
- Metrics from setup/teardown are tagged `group: ::setup` / `::teardown`; exclude them from thresholds if they skew results.
- `__VU` is 0 in init context for setup/teardown; `__ITER` counts iterations per VU.

## Gotchas
- Login per iteration inflates load on auth; log in once per VU (in a VU-scoped variable on first iteration) or in setup for shared tokens.
- `--no-setup` / `--no-teardown` flags skip them (useful for debugging); with `--no-setup` the `data` argument is `undefined`, so `data.productIds` throws a `TypeError` in the example above. Guard with `data?.productIds`.

## Verify
Seed and cleanup run exactly once (check logs), memory stays flat as VUs increase, and VU code contains no file reads.
