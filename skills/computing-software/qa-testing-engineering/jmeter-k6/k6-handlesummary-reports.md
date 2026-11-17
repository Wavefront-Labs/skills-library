---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-handlesummary-reports
name: k6-handlesummary-reports
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6, handlesummary, k6-outputs, end-of-test-summary, junit-xml, html-report, k6-reporter]
level: practitioner
status: verified
description: "Customise k6's end-of-test output with handleSummary: JSON, JUnit XML, HTML and text summaries, summaryTrendStats, and wiring results into CI."
sources:
  - https://grafana.com/docs/k6/latest/results-output/end-of-test/custom-summary/
  - https://grafana.com/docs/k6/latest/results-output/end-of-test/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k6 handleSummary

**Goal:** produce machine-readable and human-readable reports from every run.

## Example
```js
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.1.0/index.js'
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js'

export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
  thresholds: { http_req_duration: ['p(95)<300'], http_req_failed: ['rate<0.01'] },
}

export function handleSummary(data) {
  const p95 = data.metrics.http_req_duration.values['p(95)']
  return {
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
    'results/summary.json': JSON.stringify(data, null, 2),
    'results/report.html': htmlReport(data),
    'results/p95.txt': `${p95}\n`,
  }
}
```
`data.metrics.<name>.values`, `data.metrics.<name>.thresholds` (`{ 'p(95)<300': { ok: true } }`), `data.root_group.checks`, `data.state.testRunDurationMs`. All four paths were present in the object passed to `handleSummary` on k6 2.3.0 (top-level keys `options, state, metrics, setup_data, root_group`), with or without `--new-machine-readable-summary`.

The `results/` directory must already exist: k6 does not create it, and the run logs `failed to handle the end-of-test summary ... could not open 'results/summary.json'` (run). Create it in the CI step (`mkdir -p results`) before `k6 run`. The example ran cleanly on 2.3.0 once the directory existed: it wrote `summary.json`, `report.html` (k6-reporter v3.0.4 from `main`, so pin a release tag or vendor it), `p95.txt` and `junit.xml`.

## JUnit for CI
jslib `k6-summary` (0.1.0 exists on jslib.k6.io) provides `jUnit(data)` which turns thresholds into test cases: `import { jUnit } from 'https://jslib.k6.io/k6-summary/0.1.0/index.js'` and `'results/junit.xml': jUnit(data)`. Run: a passing run gave `<testsuite name="k6 thresholds" tests="2" failures="0">`; with `p(95)<0.0001` the testcase carried `<failure message="trend threshold failed: ..." />` and k6 exited 99. CI test tabs then show threshold pass/fail.

## CLI alternatives
`k6 run --summary-export=summary.json` (still present in 2.3.0; the JSON has `root_group` and `metrics` at the top level). `--no-summary` was removed in k6 v2.0.0 (`unknown flag: --no-summary`, run); use `--summary-mode=disabled` (modes: `compact`, `full`, `disabled`).

## Gotchas
- Returning an object from handleSummary replaces the default stdout summary unless you include `stdout` (run: a handleSummary returning only a file entry printed no summary).
- Remote imports need network in CI; vendor jslib files into the repo for air-gapped runners.
- Exit code still comes from thresholds (99 on threshold failure), not from handleSummary.

## Verify
CI artifacts contain the HTML and JSON, and the JUnit report shows a failed case when a threshold is breached.
