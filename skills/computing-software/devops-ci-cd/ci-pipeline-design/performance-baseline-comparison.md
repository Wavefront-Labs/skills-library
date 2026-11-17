---
id: computing-software.devops-ci-cd.ci-pipeline-design.performance-baseline-comparison
name: performance-baseline-comparison
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, performance-baseline, nonfunctional-testing, benchmark-regression]
level: advanced
status: docs-checked
description: "Detect performance regressions by comparing runs against stored history instead of fixed limits: Bencher statistical thresholds, k6 baselines and benchmark alerts."
sources: ["https://grafana.com/docs/k6/latest/using-k6/thresholds/", "https://bencher.dev/docs/explanation/thresholds/", "https://github.com/benchmark-action/github-action-benchmark", "https://grafana.com/docs/k6/latest/testing-guides/automated-performance-testing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing against baseline runs

A fixed limit such as "p95 under 200 ms" (k6 threshold: `http_req_duration: ['p(95)<200']`)
is a static pass/fail criterion; k6 exits non-zero when any threshold fails, so it can gate a
pipeline. To catch gradual regressions, compare each new result with stored history.

## k6
Grafana recommends always creating average-load tests for baseline comparisons, and smoke tests
to validate scripts before larger tests. Its automation guide lists comparing current
performance against an existing baseline as one use of automated runs, and suggests tracking
key metrics over time against their baselines. In staging it suggests running each test at
least twice consecutively so unreliable tests can be ignored.

## Bencher (statistical thresholds)
A Bencher Threshold belongs to one Branch, Testbed and Measure and uses a Test (with its
parameters, a Model) to detect regressions. A Model needs a Lower Boundary, Upper Boundary or
both: an upper boundary suits latency (larger is worse), a lower one throughput. A new
Metric outside a Boundary Limit raises an Alert. With `bencher run`:
- `--threshold-measure`, `--threshold-test`, `--threshold-upper-boundary`,
  `--threshold-lower-boundary`, `--threshold-max-sample-size`, `--threshold-min-sample-size`,
  `--threshold-window` (seconds) select the Model and its data; `--thresholds-reset` removes
  unspecified Models; `--error-on-alert` fails the command when an Alert is generated.
- Tests: `percentage`, `z_score`, `t_test`, `log_normal`, `iqr`, `delta_iqr`, `static`.
  `percentage` alerts when a value is a set percentage (0.10 is 10%) beyond the mean of
  historical metrics. z-score is recommended by the docs for at least 30 historical metrics
  and independent runs. `static` uses fixed limits and suits metrics such as code coverage.
- `--start-point-clone-thresholds` copies thresholds from the base branch for feature branches.
- Naming a benchmark with a suffix such as `_bencher_ignore` suppresses its alerts while still
  storing metrics.

## github-action-benchmark
Stores benchmark results and raises an alert when results are worse than the previous
result by more than a threshold. By default the threshold is 200% (a result 230% of the
previous is a regression); change it with `alert-threshold`. `fail-on-alert: true` fails the
job and `comment-on-alert: true` (needs a GitHub token) comments on the commit. With
`auto-push`, results are committed to a `gh-pages` branch by default.

## Verify
- [ ] The baseline is produced under the same conditions as the candidate run.
- [ ] A deliberately injected slowdown trips the alert, and an unchanged commit does not.
- [ ] Intentional regressions are accepted explicitly and become the new baseline.

## Checked
Confirmed 2026-11-09 against the Bencher thresholds page (read in full), the k6 thresholds page (threshold syntax, non-zero exit; keyword search), the k6 automated performance testing guide (baseline and smoke recommendations; keyword search), and the github-action-benchmark README (alert threshold, fail-on-alert, comment-on-alert, gh-pages; keyword search).
Removed as unconfirmed: the `k6 --summary-export` plus jq comparison, the +10% p95 and -5% throughput limits, the "3-5 repeat runs" rule, Mann-Whitney, `benchstat`, dedicated-hardware and baseline-update-on-main rules.
Method: docs-checked 2026-11-09 against bencher.dev thresholds, grafana.com k6 thresholds and automated performance testing, github-action-benchmark README
