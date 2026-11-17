---
id: computing-software.qa-testing-engineering.jmeter-k6.correlation-and-data-driven-load-tests
name: correlation-and-data-driven-load-tests
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, k6, correlation, dynamic-values, csrf-token, session-id, regular-expression-extractor, css-selector-extractor, json-extractor, csv-data-set-config, data-driven-testing, parameterization, think-time, jmeter-timers, k6-sharedarray, test-data-management, http-recording]
level: advanced
status: docs-checked
description: "Correlate dynamic server values (tokens, session IDs) between load-test requests, and drive scripts from external data files without exhausting or duplicating test accounts."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#CSV_Data_Set_Config
  - https://jmeter.apache.org/usermanual/regular_expressions.html
  - https://grafana.com/docs/k6/latest/examples/data-parameterization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correlation and data-driven load tests

**Goal:** a recorded or scripted load test that still passes when the server
issues a fresh CSRF token, session ID, or order number on every run — and that
exercises realistic account/data variety instead of every virtual user hammering
the same row.

## 1. Why naive recordings break on replay
A browser proxy recording captures the exact token value seen during recording
(e.g., `csrf_token=a1b2c3`). Replaying that value verbatim fails as soon as the
server rotates it, which is most servers, on most requests. **Correlation** means
extracting the fresh value from one response and injecting it into the next
request, every iteration.

## 2. Correlation in JMeter
Extract with a **Regular Expression Extractor**, **JSON Extractor** (JSONPath), **JSON JMESPath Extractor**, or
**CSS Selector Extractor** (formerly CSS/JQuery), attached as a child of the response that contains the
value; reference it in later samplers as `${varName}`:
```
JSON Extractor: JSON Path = $.csrfToken  ->  Variable = csrfToken
Next request body: {"token": "${csrfToken}", ...}
```
Debug with the **Debug Sampler** + **View Results Tree** in a 1-thread, 1-loop
dry run before scaling up — correlation bugs that silently fall back to an empty
variable are invisible in aggregate reports (the request still "succeeds" with a
400/401 you didn't notice because you were only watching throughput).

## 3. Correlation in k6
In k6 you write the correlation explicitly (k6 Studio, a separate recorder, is not covered here):
```js
const loginRes = http.post(`${BASE}/login`, payload)
const token = loginRes.json('csrfToken')
http.post(`${BASE}/orders`, JSON.stringify({ token }), { headers: { 'Content-Type': 'application/json' } })
```
This is explicit code rather than GUI extractors, so it stays readable and diffable in version control.

## 4. Data-driven parameterization
Don't let every virtual user log in as the same account or create the same order —
it hides lock-contention and cache-hit-rate bugs that only show up with varied
data, and many apps rate-limit or lock a single account under concurrent load
(a false "failure" that's really a one-account artifact).
- **JMeter**: `CSV Data Set Config`, by default one line per thread from a file opened once; set "Sharing mode"
  deliberately: `All threads` (the default), `Current thread group`, `Current thread` or `Identifier` (threads with the same identifier share the file). The default shares one file across all thread groups. Relative file names resolve against the test plan's path; in distributed runs the file must exist on each server. At end of file, "Recycle on EOF" restarts from the first line, and with recycle off and "Stop thread on EOF" on the thread stops; otherwise variables are set to `<EOF>`.
- **k6**: `SharedArray` loads data once and shares the memory between VUs instead of copying it per VU (the k6 docs warn that without it a large dataset can exhaust memory; it has some CPU overhead per element access).
```js
import { SharedArray } from 'k6/data'
const users = new SharedArray('users', () => JSON.parse(open('./users.json')))
```
Recycle or pool test accounts rather than creating new ones per run unless you also
clean them up — a load test that "succeeds" by leaving 50,000 orphan accounts in
the target system is a liability, not a result.

## 5. Think time
Real users pause between actions; a loop with zero delay produces an unrealistic
request rate that doesn't match the workload model this test is supposed to
represent (see `performance-testing.workload-modelling-and-bottleneck-analysis`).
JMeter: Timers (Uniform/Gaussian Random Timer). k6: `sleep(randomBetween(1, 3))`.
Derive the think-time distribution from real traffic or analytics, not a guess.

## Verify
- [ ] 1-thread dry run confirms every correlated value is non-empty and used.
- [ ] Response codes checked per-request, not just aggregate pass rate (a 400 with
      a 200-shaped body won't show up as a JMeter/k6 "error" by itself).
- [ ] CSV/data sharing mode set deliberately, confirmed across thread groups/VUs.
- [ ] Test accounts/data cleaned up or pooled after the run.
- [ ] Think-time distribution matches a real traffic sample, not zero or a flat constant.

## Checked
Checked against the Grafana k6 docs sources (grafana/k6-docs, docs/sources/k6/next, last commit 2026-10-13, which document k6 v2) and the k6 Operator repository (grafana/k6-operator, last commit 2026-10-21). Also Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01). Confirmed: JMeter extractor component names, Debug Sampler, CSV Data Set sharing modes, default and EOF behaviour, relative-path rule, `SharedArray` guidance in the k6 data parameterization docs. The k6 and JMeter snippets were not run, and the k6 `Response.json()` selector call was not checked.

Method: documentation only; no commands were run.
