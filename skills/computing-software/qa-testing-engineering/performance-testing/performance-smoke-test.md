---
id: computing-software.qa-testing-engineering.performance-testing.performance-smoke-test
name: performance-smoke-test
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [performance-smoke-test, smoke-testing, load-testing, script-validation, k6]
level: practitioner
status: verified
description: "Run a performance smoke test before any load test: minimal VUs to validate the script, data, checks and environment, baseline single-user timings, and a CI gate."
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/smoke-testing/
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smoke performance test as a script sanity gate

**Goal:** prove the script and environment work, and capture single-user baseline timings, before spending hours on a load test.

## What it checks
- Script runs end to end without errors (correlation, auth, data files).
- All checks pass at minimal load; error rate 0%.
- Environment is up and the right version is deployed.
- Baseline latency with no contention (later load results compare against it).
- Generator and monitoring wiring (outputs, dashboards, test id tags) work.

## k6 example
```js
export const options = {
  vus: 1, duration: '1m',              // or iterations: 5
  thresholds: {
    checks: ['rate==1.0'],
    http_req_failed: ['rate==0'],
    http_req_duration: ['p(95)<800'],
  },
};
```
```bash
k6 run -e PROFILE=smoke -e BASE_URL=$TARGET script.js
```
`__ENV.BASE_URL` and `__ENV.PROFILE` read those `-e` values (the example above used `${__ENV.BASE_URL}` in the request URL). When a threshold fails k6 exits with code 99, which fails a CI step; a smoke run that passes exits 0. k6's docs describe smoke tests as a few VUs (more than 5 is a mini-load test) for iterations or seconds to a few minutes.
JMeter: 1 thread, 1-5 loops in CLI mode (`jmeter -n -t test.jmx -l test.jtl`, per the JMeter best practices) with the same assertions. Locust: `-u 1 -r 1 -t 1m --headless`.

## Where it runs
- On every change to the load scripts (PR) to keep scripts working.
- On every deploy to a performance environment as a pre-flight before the scheduled load test.
- Optionally every PR against an ephemeral environment as a cheap regression signal on single-user timings.

## Read results
- Any failure = fix script or environment before load testing.
- Record per-transaction single-user times; if a transaction is already slow at 1 user, load will not help; report it immediately.

## Gotchas
- Smoke run against stale data (expired tokens, deleted fixtures) fails for test reasons; refresh data in setup.
- Do not compare smoke timings against production SLOs with cold caches; run a couple of warm-up iterations.

## Verify
Smoke passes with 100% checks before every load run, and its baseline timings are stored with the test results.

## Checked
k6 v1.4.0 and Locust 2.47.0 on Windows against a local stdlib HTTP server.
- Run: the k6 options block with `iterations: 5` and `__ENV.BASE_URL`: all three thresholds (`checks` rate==1.0, `http_req_failed` rate==0, `http_req_duration` p(95)<800) passed with exit code 0; changing the p95 limit to 0.001 ms gave exit code 99; the `vus: 1, duration` form ran 1 VU for 3 s. Locust `-u 1 -r 1 -t` form is covered by the other Locust runs in this batch.
- Fetched: k6 smoke-testing guide (few VUs, more than 5 is a mini-load test, run when scripts change and after deploys) and JMeter best-practices page (CLI mode command).
- JMeter: the skill states only the CLI command, copied from the fetched JMeter best-practices page.
