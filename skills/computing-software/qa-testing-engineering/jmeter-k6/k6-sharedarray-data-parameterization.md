---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-sharedarray-data-parameterization
name: k6-sharedarray-data-parameterization
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [sharedarray, k6-data-parameterization, papaparse, k6-test-data, unique-data-per-vu]
level: practitioner
status: verified
description: "Parameterise k6 tests with SharedArray (JSON/CSV via papaparse), pick rows per VU or iteration uniquely using exec.vu and exec.scenario, and avoid per-VU memory blowup."
sources:
  - https://grafana.com/docs/k6/latest/javascript-api/k6-data/sharedarray/
  - https://grafana.com/docs/k6/latest/examples/data-parameterization/
  - https://grafana.com/docs/k6/latest/javascript-api/k6-execution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data parameterization with SharedArray

## Why SharedArray
Each VU has its own JS runtime; a plain `JSON.parse(open('users.json'))` copies the data into every VU (1,000 VUs x 50 MB = trouble). `SharedArray` loads once in init and shares a read-only copy.

```js
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

const users = new SharedArray('users', () => JSON.parse(open('./data/users.json')));
const products = new SharedArray('products', () =>
  papaparse.parse(open('./data/products.csv'), { header: true, skipEmptyLines: true }).data);
```
The function must return an array (anything else fails with `only arrays can be made into SharedArray`). Elements are read-only: `users[0].email = 'x'` throws `TypeError: Cannot assign to read only property 'email'` and `Object.isFrozen(users[0])` is true (run on k6 2.3.0). Copy first (`const u = { ...users[0] }`) if you need to modify a row.

## Selecting rows
```js
import exec from 'k6/execution';
export default function () {
  const user = users[exec.vu.idInTest % users.length];                         // stable per VU
  const product = products[exec.scenario.iterationInTest % products.length];   // unique per iteration across VUs
  const randomOne = users[Math.floor(Math.random() * users.length)];
}
```
- `exec.vu.idInTest`: 1-based VU id across the test (and across instances in distributed runs). Run: with 3 users, VU 1 got `users[1]`, so row 0 is first used by VU 3; use `(exec.vu.idInTest - 1) % users.length` to start at row 0.
- `exec.scenario.iterationInTest`: 0-based unique iteration number within the scenario (run: a `shared-iterations` scenario with 2 VUs and 6 iterations saw 0..5, each once), good for "use each record once" (pair with `shared-iterations` and `iterations = data.length`).

## Data volume planning
Unique-per-iteration data needs at least `rate x duration` rows for arrival-rate tests. Running out means reuse, which can hit caches or "already used" business errors.

## Gotchas
- `open()` only works in init context (in VU code: `the "open" function is only available in the init stage`), paths relative to the script.
- SharedArray name must be unique per dataset: a second `new SharedArray('x', ...)` with a name already used does not fail, it returns the first dataset's data (run: `[2,3]` came back as `[1]`).
- `new SharedArray` outside init throws `new SharedArray must be called in the init context`.
- CSV numbers arrive as strings with papaparse unless `dynamicTyping: true` (run: `typeof price` was `string`, then `number`; `skipEmptyLines: true` dropped the blank row, 3 products).
- Don't put secrets in data files committed to git.

## Verify
Memory per VU stays flat as VU count grows (watch k6 process RSS); server logs show distinct users.
