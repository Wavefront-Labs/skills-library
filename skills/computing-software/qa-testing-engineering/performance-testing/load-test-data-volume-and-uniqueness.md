---
id: computing-software.qa-testing-engineering.performance-testing.load-test-data-volume-and-uniqueness
name: load-test-data-volume-and-uniqueness
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [load-test-data, data-volume-planning, unique-test-data, data-exhaustion]
level: practitioner
status: verified
description: "Plan test data for load tests: database size parity, number of unique records consumed per run, popularity distributions, data reset between runs and avoiding cache-friendly data."
sources:
  - https://grafana.com/docs/k6/latest/examples/data-parameterization/
  - https://jmeter.apache.org/usermanual/component_reference.html#CSV_Data_Set_Config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test data volume and uniqueness for load tests

## Two different data needs
1. **Background volume:** the database must be production-sized (rows, index sizes, data distribution). A query fast on 10k rows can be slow on 50M. Load via masked production snapshots or generators.
2. **Consumed data:** records each iteration uses (logins, products, coupons, one-time tokens).

## Sizing consumed data
| Data type | Needed |
|---|---|
| User accounts (concurrent sessions) | ≥ peak concurrent VUs (avoid two VUs sharing a session) |
| One-time items (coupons, invites, payments with unique refs) | ≥ total iterations = rate x duration |
| Lookup keys (product ids) | enough to mirror real cache hit ratio |

Example: 50 checkouts/s for 30 min = 50 x 1,800 s = 90,000 unique payment references (computed).

## Distribution matters
Real access is skewed (Zipf-like): a few products get most views. Uniform random ids over a huge catalogue give a too-low cache hit rate; always hitting 10 ids gives too high. Sample from production popularity (top-N weights) when possible.

## Reset between runs
- Restore a DB snapshot before each run (fastest consistent approach).
- Or create-then-delete in setup/teardown with bulk APIs.
- Track data consumption: tests failing late with "coupon already used" means exhaustion.

## Implementation pointers
k6 SharedArray + `exec.scenario.iterationInTest` (an index that is unique across VUs within a scenario run); JMeter CSV Data Set Config (Sharing mode: All threads, which is the default; Recycle on EOF: false and Stop thread on EOF: true for one-time data; Stop thread on EOF only applies when Recycle is false); Locust per-worker partitions.
```js
import http from 'k6/http';
import { SharedArray } from 'k6/data';
import exec from 'k6/execution';
const refs = new SharedArray('refs', () => Array.from({ length: 90000 }, (_, i) => `ref-${i}`));
export const options = { scenarios: { s: { executor: 'shared-iterations', vus: 3, iterations: 20 } }, discardResponseBodies: true };
export default function () {
  http.get(`http://localhost:8080/pay?ref=${refs[exec.scenario.iterationInTest]}`);   // iteration 19 used ref-19
}
```
Running out of rows is silent in this form (`refs[n]` becomes undefined past the end), so size the array to rate x duration or stop the scenario when the data runs out.

## Gotchas
- Accounts with MFA, captcha, or rate-limited login break under load: use test bypass flags agreed with security.
- Data created during tests (orders) grows tables: long soak tests should include cleanup or account for growth.

## Verify
Pre-run checklist confirms DB row counts vs production, consumed-data count ≥ planned iterations, and snapshot restored.

## Checked
k6 v1.4.0 on Windows against a local stdlib HTTP server; fetched docs.
- Run: a shared-iterations scenario with a `SharedArray` and `exec.scenario.iterationInTest`: 20 iterations over 3 VUs, the last iteration (index 19) used `ref-19`, no duplicates needed beyond one row per iteration; `discardResponseBodies` set `r.body` to null; `refs[5]` on a 2-element SharedArray gave undefined.
- Computed: 50 x 30 x 60 = 90,000.
- Fetched: k6 data-parameterization page (SharedArray memory behaviour), JMeter component reference (CSV Data Set Config: Recycle on EOF default true, Stop thread on EOF default false and only when Recycle is false, Sharing mode options with All threads as default).
