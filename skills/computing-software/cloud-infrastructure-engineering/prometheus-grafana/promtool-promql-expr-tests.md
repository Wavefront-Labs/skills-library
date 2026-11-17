---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promtool-promql-expr-tests
name: promtool-promql-expr-tests
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql-expr-test, promtool-test-rules, recording-rules, input-series, rule-unit-tests]
level: practitioner
status: verified
description: "Unit-test recording rules and PromQL expressions with promtool promql_expr_test: input_series notation, eval_time, exp_samples and common failure messages."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/", "https://prometheus.io/docs/prometheus/latest/command-line/promtool/", "https://prometheus.io/docs/practices/rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# promtool promql_expr_test

```yaml
# tests/http_rules_test.yml
rule_files: [../rules/http.yml]
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'http_requests_total{job="api", instance="a", code="200"}'
        values: '0+60x20'          # 0, 60, 120 ... every 1m: 1 req/s
      - series: 'http_requests_total{job="api", instance="b", code="500"}'
        values: '0+6x20'           # 0.1 req/s
      - series: 'flaky{job="x"}'
        values: '1 _ _ 4 stale'    # _ = missing sample, stale = staleness marker
    promql_expr_test:
      - expr: job:http_requests:rate5m{job="api"}
        eval_time: 10m
        exp_samples:
          - labels: 'job:http_requests:rate5m{job="api"}'
            value: 1.1
      - expr: job:http_requests:rate5m{job="nope"}
        eval_time: 10m
        exp_samples: []           # asserts empty result
```
Run: `promtool test rules tests/*.yml`.

## Notation
- `a+bxn`: start a, add b, n more samples (n+1 total). `a-bxn` decreases.
- `axn` or `a+0xn`: constant, n+1 samples (`1x5` has six; checked with `count_over_time`).
- `_` missing; `stale` staleness marker.
- Native histograms: `{{schema:0 sum:5 count:4 buckets:[1 2 1]}}` notation.

## Common failures
- `expected: ... got: ...` value mismatch from rate extrapolation: choose eval_time well inside the series, and compute expected values by hand.
- Labels mismatch: exp_samples must include every output label including `__name__` via the metric name in the string.
- Float formatting: values compare almost exactly (about 1e-16 relative): `0.0909090909` failed against `0.0909090909090909`. Write the full-precision value promtool prints in the `got:` line, or design inputs whose results are exact (the `1.1` example passes).

## Tips
- Test edge cases: no traffic (expect empty or NaN), counter reset (`0+60x5 0+60x5`), label absent.
- Keep tests next to rules in CI with `promtool check rules`.

## Verify
- [ ] CI fails when a recording rule's expression changes output.

## Checked
Run on Windows 11 with promtool 3.15.0 (Prometheus 3.15.0 windows-amd64 release): the example test file (`job:http_requests:rate5m{job="api"}` = `1.1` at 10m passes; `{job="nope"}` with `exp_samples: []` passes), `_` and `stale` handling (`flaky` returns 1 at 1m, 4 at 3m, nothing after the stale marker at 4m), decreasing series `10-2x4`, constants `7x3` and `7+0x3`, a counter reset series `0+60x5 0+60x5` (rate at 9m was 0.75, not 1: extrapolation across the reset, so hand-compute carefully), `sum(rate(...))` with `labels: '{}'`, native histogram input `{{schema:0 sum:5 count:4 buckets:[1 2 1]}}x3` with `histogram_count`, and the tolerance behaviour above. Not run: Linux, CI integration.
