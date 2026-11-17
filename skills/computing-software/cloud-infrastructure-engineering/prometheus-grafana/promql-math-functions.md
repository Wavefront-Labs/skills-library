---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-math-functions
name: promql-math-functions
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql-math-functions, sgn-function, promql, abs, ln, log2, clamp-functions]
level: practitioner
status: verified
description: "Use PromQL math functions (abs, ceil, floor, exp, ln, log2, log10, sqrt, sgn, trig, deg/rad) for normalising, log scales and sign tests, with NaN/Inf behaviour."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/", "https://prometheus.io/docs/prometheus/latest/querying/functions/#trigonometric-functions", "https://prometheus.io/docs/prometheus/latest/querying/basics/#float-literals-and-time-durations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PromQL math functions

All take an instant vector and apply element-wise, dropping the metric name.

| Function | Typical use |
|---|---|
| `abs(v)` | magnitude of drift: `abs(node_timex_offset_seconds) > 0.05` |
| `ceil(v)`, `floor(v)`, `round(v, to)` | integer counts for display; `round(x, 0.5)` |
| `sqrt(v)` | combine variances: `sqrt(sum(stdvar_metric))` |
| `exp(v)`, `ln(v)`, `log2(v)`, `log10(v)` | log-scale comparisons, orders of magnitude: `log10(rate(x[5m]))` |
| `sgn(v)` | sign (-1, 0, 1): direction of change `sgn(deriv(queue_depth[10m]))` |
| `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, ... , `deg(v)`, `rad(v)`, `pi()` | geo/angle maths, rarely needed |
| `clamp(v, min, max)`, `clamp_min`, `clamp_max` | bound noisy ratios to [0,1] |

## Examples
```promql
# 1 if growing, -1 if shrinking, over 30 min
sgn(delta(queue_depth[30m]))
# orders of magnitude change week over week
log10(sum(rate(http_requests_total[1h]))) - log10(sum(rate(http_requests_total[1h] offset 1w)))
```

## NaN and Inf
- `ln(0)` = -Inf, `ln(-1)` = NaN, `x/0` = +Inf or NaN. Comparisons with NaN are false; with +Inf behave numerically.
- To drop NaN samples use `x == x`: NaN fails every comparison, including with itself.

## Gotchas
- The metric name is dropped; use `label_replace` or recording rules to name results.
- `round()` resolves ties by rounding up (per the function docs; 3.15.0: `round(2.5)` = 3 and `round(-2.5)` = -2); `round(x, 0.1)` rounds to the nearest multiple of 0.1.
- `deg()`, `rad()` and the other trig functions take an instant vector, so `deg(pi())` is a parse error (`expected type instant vector in call to function "deg", got scalar`); wrap the scalar with `vector(pi())`.

## Checked
Run on Prometheus 3.15.0: `ln` of 0 returned -Inf and of -1 NaN, `sqrt(-1)` NaN, `vector(1) / 0` +Inf and `vector(0) / 0` NaN; `xv == xv` dropped the NaN series and kept the other; `sgn(-1)` = -1; `log2(4)` = 2; `rad(90)` = 1.5708; `clamp_min(0, 1e-9)` = 1e-09; `abs()` returned the series without `__name__`.

## Verify
- [ ] Rules using `ln`/`log*` guard against zero inputs (`clamp_min(x, 1e-9)`).
