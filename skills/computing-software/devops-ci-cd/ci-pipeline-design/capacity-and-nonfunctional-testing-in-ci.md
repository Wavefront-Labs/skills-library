---
id: computing-software.devops-ci-cd.ci-pipeline-design.capacity-and-nonfunctional-testing-in-ci
name: capacity-and-nonfunctional-testing-in-ci
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, capacity-testing, performance-testing-in-ci, load-testing-pipeline, nonfunctional-testing, k6, thresholds, soak-test, stress-test, spike-test, continuous-benchmarking]
level: advanced
status: docs-checked
description: "Put load, soak and benchmark tests in the pipeline without false alarms: k6 thresholds as gates, which environment and cadence per test type, and benchmark alerts."
sources: ["https://grafana.com/docs/k6/latest/using-k6/thresholds/", "https://grafana.com/docs/k6/latest/testing-guides/automated-performance-testing/", "https://github.com/benchmark-action/github-action-benchmark"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity and non-functional testing in CI

**Goal:** a performance regression is caught by the pipeline before a release, with a
number you trust.

## 1. Test types (k6 guide)
Smoke (script errors, minimal traffic), average-load (normal traffic), stress (maximum
expected traffic), spike (a surge) and soak (a prolonged period). Grafana recommends always
creating average-load tests for baseline comparisons and smoke tests to validate scripts
before larger tests.

## 2. Where and how often (k6 automation guide)
Automation is about running tests frequently and consistently, from CI/CD pipelines and
nightly jobs, or by manual trigger; CI is not the only way to schedule them.
- **Development:** smoke tests; scheduling them on project changes is possible.
- **QA:** often a low-scale staging environment, unsuitable for judging performance and
  scalability; run smoke tests in the CI flow to catch errors and confirm the script can later
  run at larger load.
- **Pre-release and ephemeral environments:** run larger tests with quality gates, pass or
  fail criteria validating SLOs. Keep the environment for a few hours or days; run the
  existing average-load, stress and spike tests.
- **Staging:** suitable for trends, regressions and improvements; start with a few tests two
  to three times per week, run each at least twice consecutively to discard unreliable
  tests, and scale the workload to the staging infrastructure.
- **Production:** smoke tests as synthetic monitoring (the guide suggests every five minutes
  with alerting, for example after six consecutive failures); optionally nightly or
  low-traffic tests at about half the average load, weekly. Be careful with test data and
  impact on real users.

## 3. k6 thresholds as the pipeline gate
Thresholds codify SLOs. In `options.thresholds`, key a metric to expression strings:
```js
export const options = {
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<200'],
  },
};
```
When every threshold passes k6 exits with code 0; if any fails, it exits non-zero, so the
job fails. The long format takes an object with `threshold`, `abortOnFail` and
`delayAbortEval` (for example `'10s'`) to stop a test early. Trend aggregations include
`avg`, `min`, `max`, `med` and `p(N)`; thresholds can use tags, such as
`'http_req_duration{type:staticContent}': ['p(99)<250']`.

## 4. Benchmark regression detection
`github-action-benchmark` stores benchmark results and alerts when a result is worse than the
previous by more than a threshold (default 200%, set with `alert-threshold`);
`fail-on-alert: true` fails the job and `comment-on-alert: true` comments on the commit.
See the baseline comparison skill for Bencher's statistical thresholds.

## Verify
- [ ] Each environment runs only the test types that suit it, at a stated cadence.
- [ ] Thresholds reflect SLOs, and a failure fails the job.
- [ ] Larger tests run twice before a result is trusted.

## Checked
Confirmed 2026-11-09 against the k6 thresholds page (threshold syntax, exit codes, abortOnFail, delayAbortEval, aggregations, tagged example), the k6 automated performance testing guide (test types, per-environment guidance, frequencies) and the github-action-benchmark README (alert threshold, fail-on-alert, comment-on-alert); read by keyword search with surrounding lines.
Removed as unconfirmed: the three-tier table with per-PR cadence, hosted-runner noise figure, CPU governor advice, the ramping-arrival-rate scenario, `--summary-export` and Prometheus output flags, Gatling, Locust and JMeter equivalents, criterion and Codspeed advice, Lighthouse CI, soak queries, chaos steps, and the 5% noise budget. The Humble and Farley chapter and the criterion book were not read and were dropped from `sources`.
Method: docs-checked 2026-11-09 against grafana.com k6 thresholds and automated performance testing guide, github-action-benchmark README
