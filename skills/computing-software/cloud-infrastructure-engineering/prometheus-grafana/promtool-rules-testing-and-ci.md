---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promtool-rules-testing-and-ci
name: promtool-rules-testing-and-ci
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, promtool, promtool-check-rules, rule-linting, promtool-test-rules, input-series, alert-rule-test, rules-ci-pipeline, rules-linting-ci, pint, rule-unit-tests]
level: practitioner
status: verified
description: "Lint and unit-test Prometheus rules in CI: promtool check rules, test files with input_series and alert_rule_test, expanding notation, pint for live checks, and a pipeline layout."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/", "https://prometheus.io/docs/prometheus/latest/command-line/promtool/", "https://cloudflare.github.io/pint/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Prometheus rules in CI

## Lint
```bash
promtool check rules rules/*.yml          # syntax, PromQL parse, duplicate rules
promtool check rules --lint=all --lint-fatal rules/*.yml   # duplicate-rules etc. as failures (exit code 3)
# without --lint-fatal a duplicate rule prints "FAILED: lint error ..." but the exit code is still 0; a parse error exits 1
```

## Unit tests
```yaml
# tests/http_test.yml
rule_files: [../rules/http.yml]
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'http_requests_total{job="api",code="200"}'
        values: '0+100x30'            # 0,100,200,... 31 samples
      - series: 'http_requests_total{job="api",code="500"}'
        values: '0+10x30'             # 10/min errors -> ~9% error ratio
    promql_expr_test:
      - expr: job:http_request_errors:ratio_rate5m
        eval_time: 10m
        exp_samples:
          - labels: 'job:http_request_errors:ratio_rate5m{job="api"}'
            value: 0.0909090909090909     # compared (almost) exactly: 0.0909090909 fails
    alert_rule_test:
      - eval_time: 4m
        alertname: HighErrorRate
        exp_alerts: []                # 'for: 5m' not yet satisfied
      - eval_time: 15m
        alertname: HighErrorRate
        exp_alerts:
          - exp_labels: {severity: page, job: api}
            exp_annotations: {summary: "api error ratio 9.091%"}   # if the rule uses humanizePercentage
```
```bash
promtool test rules tests/*.yml
```
Notation: `a+bxN` (start a, add b, N more samples), `a-bxN`, `_` = missing sample, `stale` = staleness
marker, `1x5` = six 1s (the `x` count is the number of *additional* samples, like `1+0x5`). `exp_annotations` must match exactly (rendered templates).

## Live checks with pint
`pint lint rules/` (static) and `pint ci --base-branch=main` check rules against a running Prometheus:
metrics that don't exist, labels absent from the data, `rate` on gauges, missing `for`, cost of queries.

## Pipeline
1. `promtool check rules` + `pint lint` on every PR.
2. `promtool test rules` for every file with alerts (require a test per alert in review).
3. For PrometheusRule CRs, extract `.spec` with yq before running promtool.
4. Deploy; post-deploy check that `prometheus_rule_evaluation_failures_total` didn't increase.

## Verify
- [ ] CI fails on a deliberately broken expression and on a changed alert threshold without updated tests.
- [ ] Each alert has at least one firing and one non-firing test case.

## Checked
Run on Windows 11 with promtool 3.15.0 (Prometheus 3.15.0 windows-amd64 release): `check rules` on a three-rule file (SUCCESS), a PromQL syntax error (`parse error: unexpected "(" in grouping opts`, exit 1), duplicate recording rules (printed as `FAILED: lint error 1 duplicate rule(s) found` with exit 0 by default, exit 3 with `--lint=all --lint-fatal`); `test rules` with this skill's input series: the recording rule and `for: 5m` alert behaved as described (no alert at 4m and 5m, firing at 6m and 15m), a rule using `humanizePercentage` rendered `9.091%` (the skill's `9.09%` fails the exact annotation match), and the expected value `0.0909090909` failed while `0.0909090909090909` passed (`0.09090909090909091`, `0.090909090909091` and `0.09090909091` all failed: the comparison is essentially exact); series notation counted with `count_over_time`: `0+100x30` gives 31 samples, `1x5` and `1+0x5` give 6, `10-2x4` gives 5, `_` and `stale` drop samples. Not run: `pint`, yq extraction from PrometheusRule CRs, the post-deploy metric check. promtool output and exit codes were not compared on Linux.
