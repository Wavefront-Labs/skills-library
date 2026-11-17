---
id: computing-software.qa-testing-engineering.performance-testing.load-test-error-analysis
name: load-test-error-analysis
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [load-error-analysis, error-rate-under-load, error-classification, timeout-analysis]
level: practitioner
status: verified
description: "Analyse load-test errors: classify status codes, timeouts and connection errors, separate generator-side from server-side failures, and find when and where they start."
sources:
  - https://grafana.com/docs/k6/latest/javascript-api/error-codes/
  - https://jmeter.apache.org/usermanual/generating-dashboard.html
  - https://docs.locust.io/en/stable/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error rate analysis under load

## Classify first
| Class | Examples | Typical meaning |
|---|---|---|
| HTTP 5xx | 500, 502, 503, 504 | app errors, upstream/LB overload, gateway timeouts |
| HTTP 429 | rate limiting | protective throttling (expected?) |
| HTTP 4xx (other) | 401, 404, 409 | script/data problems (expired tokens, used coupons) more often than load issues |
| Client timeout | k6 `request timeout` (1050), JMeter connect/response timeout errors | server too slow or connection stuck |
| Connection errors | `connection reset by peer` (1220), `dial: connection refused` (1212), `dial tcp ...: i/o timeout` (1211), `socket: too many open files` | LB/server dropping connections, port/file-descriptor exhaustion |
| Assertion/check failures | wrong body under load | stale cache, partial responses, race conditions |

k6 gives `error_code` tags: 1050 request timeout, 1211 dial timeout, 1212 dial connection refused, 1220 connection reset by peer, 1400-1499 for HTTP 4xx and 1500-1599 for HTTP 5xx (a 500 gave 1500, a 404 gave 1404, a refused port gave 1212 and `error` "dial: connection refused", a 50 ms timeout gave 1050 "request timeout"); JMeter dashboard has an error table and "Top 5 Errors by Sampler"; Locust writes `<prefix>_failures.csv` (Method, Name, Error, Occurrences, First Seen, Last Seen) with `--csv`.

## When and where
- Plot error rate over time against load steps: errors from the first second = script/data bug; errors starting at a load level = capacity limit; errors after hours = leak/exhaustion.
- Break down by endpoint (`name` tag) and by status: a single endpoint failing points to its dependency.
- Correlate with server logs and LB metrics (target 5xx vs LB 5xx distinguishes app errors from LB-generated ones).

## Generator vs server
- Generator-side: high CPU, ephemeral port exhaustion (the OS reports it as a connect or dial error; the k6 guide lists the OS tuning), too many open files (`socket: too many open files` in k6), DNS failures. Fix with more generators, `ulimit -n`, keep-alive, wider port range.
- Server-side: errors recorded in server/LB logs at the same timestamps.

## Report
Error budget against SLO (e.g. < 0.5%), top error types with counts and first occurrence time, root cause per type, and whether retries in clients would mask them in production.

## Gotchas
- Averaging error rate over the whole run hides a 5-minute outage; always look at the time series.
- Treating 4xx data errors as load errors leads to wrong capacity conclusions; fix the script and rerun.

## Verify
Every error class in the results has an explanation (script, generator, or system) with evidence.

## Checked
k6 v1.4.0 and Locust 2.47.0 on Windows against a local stdlib HTTP server.
- Run: a k6 script requesting a closed port, a slow path with `timeout: '50ms'`, a 500 path and a 404 path printed `error_code` 1212, 1050, 1500 and 1404; Locust `--csv` produced `_failures.csv` with the header quoted above.
- Fetched: k6 error-codes page (ranges and the 1050/1211/1212/1220 definitions; the old skill text called 1220 connection refused, which is wrong), k6 running-large-tests page (the `dial tcp ...: i/o timeout` and `socket: too many open files` error messages), JMeter dashboard page (error table and Top 5 Errors by Sampler).
