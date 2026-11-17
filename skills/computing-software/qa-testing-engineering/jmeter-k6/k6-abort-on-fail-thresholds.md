---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-abort-on-fail-thresholds
name: k6-abort-on-fail-thresholds
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [abortonfail, k6, thresholds, test-abort, ci-quality-gates]
level: practitioner
status: verified
description: "Stop k6 tests early when they are clearly failing: abortOnFail thresholds with delayAbortEval, exec.test.abort(), exit codes for CI, and protecting shared environments."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/thresholds/#abort-a-test-when-a-threshold-is-crossed
  - https://grafana.com/docs/k6/latest/javascript-api/k6-execution/#test
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# abortOnFail thresholds and test abort (k6)

**Goal:** do not keep hammering a system that is already failing; save time and protect shared environments.

## abortOnFail
```js
export const options = {
  scenarios: { load: { executor: 'ramping-arrival-rate', startRate: 10, timeUnit: '1s', preAllocatedVUs: 200,
                       stages: [{ target: 200, duration: '15m' }, { target: 200, duration: '30m' }] } },
  thresholds: {
    http_req_failed: [{ threshold: 'rate<0.05', abortOnFail: true, delayAbortEval: '1m' }],
    http_req_duration: [
      'p(95)<500',                                                     // fail at end, no abort
      { threshold: 'p(99)<3000', abortOnFail: true, delayAbortEval: '2m' },
    ],
  },
};
```
- Thresholds are evaluated periodically (every 2 s, `thresholdsRate` in `internal/metrics/engine/engine.go`); `delayAbortEval` waits for enough samples so a slow first request does not abort the run. In Grafana Cloud k6 thresholds are evaluated every 60 s, so an abort can lag by up to a minute.
- On a threshold abort during the run, teardown still runs and the summary is printed (run on k6 2.3.0: error `thresholds on metrics 'http_req_failed' were crossed; at least one has abortOnFail enabled, stopping test prematurely`, exit 99, `teardown()` executed).

## Abort from code
```js
import exec from 'k6/execution';
export default function () {
  const res = http.get(`${BASE}/health`);
  if (res.status === 503 && res.headers['Retry-After']) {
    exec.test.abort('system in maintenance, aborting');
  }
}
```
In setup: abort if preconditions fail (seed failed, wrong environment). Teardown does NOT run when `setup()` aborts (run: exit 108, no teardown output), so do not rely on it to clean up work done before the abort call:
```js
export function setup() {
  if (!__ENV.BASE_URL.includes('staging')) exec.test.abort('refusing to run against non-staging target');
}
```

## Exit codes (for CI)
- `0` all thresholds passed.
- `99` thresholds failed (`ThresholdsHaveFailed`).
- `108` aborted by script (`exec.test.abort`); `107` script exception; `100`/`101` setup/teardown timeout; `104` invalid config; `110` test marked as failed from script. Full list: `errext/exitcodes/codes.go` in the k6 repo.
- Verified by running k6 2.3.0 against a local server: abortOnFail threshold gave 99, `exec.test.abort()` in the default function and in `setup()` gave 108.
CI should fail on any non-zero code and keep the summary/output artifacts.

## Gotchas
- Very short `delayAbortEval` aborts on warm-up noise (cold caches, JIT).
- Aborting stress or breakpoint tests on errors defeats their purpose; use abort for safety limits (e.g. error rate > 50%) only.

## Verify
A deliberately broken endpoint aborts the run within the expected time with exit code 99 or 108, and teardown cleanup still executes.
