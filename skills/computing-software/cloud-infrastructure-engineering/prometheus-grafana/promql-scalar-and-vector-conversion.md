---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-scalar-and-vector-conversion
name: promql-scalar-and-vector-conversion
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [scalar-function, vector-function, promql, binary-operators, or-vector-zero]
level: practitioner
status: verified
description: "Convert between scalars and vectors in PromQL with scalar() and vector(): fallback values, comparing to a single series, and the NaN result when scalar() gets 0 or 2+ series."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#scalar", "https://prometheus.io/docs/prometheus/latest/querying/functions/#vector", "https://prometheus.io/docs/prometheus/latest/querying/operators/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scalar() and vector()

- `scalar(v instant-vector)`: returns the sample value of a single-element vector as a scalar; if the input does not have exactly one element, returns `NaN`.
- `vector(s scalar)`: returns the scalar as a vector with no labels.

## Uses
```promql
# compare every instance against a cluster-wide single value
node_load1 > scalar(avg(node_load1)) * 2

# fallback when a series is missing (labels lost)
sum(rate(errors_total[5m])) or vector(0)

# constant thresholds as series for recording rules / graphs
vector(0.999)

# use time as a vector
vector(time()) - max(job_last_success_timestamp_seconds)
```

## Gotchas
- `scalar()` of an empty or multi-series result is `NaN`; comparisons with NaN are always false, so an alert silently never fires. Aggregate to one series first (`scalar(sum(...))`).
- `or vector(0)` only works when the left side has no labels (after `sum()`); with labels, the `vector(0)` series (no labels) is added as an extra series rather than filling gaps per group.
- Scalar-to-vector arithmetic keeps the vector's labels; vector-to-vector needs matching.
- Grafana stat panels show `NaN` from scalar(); prefer instant vectors.

## Checked
Run on Prometheus 3.15.0: `scalar()` of a single series returned its value, of two series and of an empty result returned NaN; `node_load1 > scalar(avg(node_load1)) * 2` returned only the series above twice the mean; `sum(rate(nonexist[5m])) or vector(0)` returned 0; with `sum by (job)` on the left the `vector(0)` fallback is a label-less series.

## Verify
- [ ] Alert expressions using `scalar()` are tested with promtool for the empty-input case.
