---
id: computing-software.data-engineering.data-quality.distribution-drift-monitoring
name: distribution-drift-monitoring
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-observability, distribution-drift, field-level-monitoring, psi, null-rate, category-shift, profiling]
level: advanced
status: gated
description: "Monitor field-level distributions for silent breakage: null and zero rates, category mix, quantiles, PSI/KS drift scores, seasonal baselines and alert tuning."
sources:
  - https://docs.databricks.com/en/lakehouse-monitoring/index.html
  - https://docs.elementary-data.com/data-tests/anomaly-detection-tests/all-columns-anomalies
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distribution drift monitoring

**Goal:** catch breakages that pass schema and not-null tests: a country column suddenly 40% "US" instead of 10%, amounts in cents instead of dollars, a feature stuck at 0.

## Metrics to track per column per period
| Column type | Metrics |
|---|---|
| any | null rate, row count, distinct count |
| numeric | mean, p01/p50/p99, min/max, zero rate, negative rate |
| categorical | share per top-N category, new/unseen categories, "other" share |
| text | empty-string rate, avg length, pattern conformance rate |
| timestamp | share in future, lag vs load time |

Compute daily into a metrics table:
```sql
insert into dq.column_profile
select current_date, 'orders', 'amount',
  count(*), avg(case when amount is null then 1 else 0 end),
  approx_percentile(amount, 0.5), approx_percentile(amount, 0.99),
  avg(case when amount = 0 then 1 else 0 end)
from sales.orders where order_date = current_date - 1;
```

## Drift scores
- **PSI (population stability index)** for binned numeric or categorical distributions:
  `PSI = sum((p_i - q_i) * ln(p_i / q_i))` over bins; < 0.1 stable, 0.1-0.25 moderate, > 0.25 significant (industry rules of thumb, not from a standard (gated: unconfirmed, source is paywalled or blocked)). Check the function below: identical inputs give 0.0; [.25]*4 vs [.4,.2,.2,.2] gives 0.104; an empty bin (50/50 vs 0/100) gives 9.2 because of the eps smoothing, so merge sparse bins first.
- **KS statistic** (two-sample) for numeric distributions; Jensen-Shannon distance for categorical.
```python
import numpy as np
def psi(expected, actual, eps=1e-6):
    e = np.asarray(expected) + eps; a = np.asarray(actual) + eps
    e, a = e / e.sum(), a / a.sum()
    return float(np.sum((a - e) * np.log(a / e)))
```

## Baselines
- Compare to the same weekday over the last 4-8 weeks, not just yesterday (weekly seasonality).
- Exclude known event days (holidays, promotions) or use wider bands then.
- Use z-scores / MAD on the metric time series for single metrics (null rate, mean), PSI for whole distributions.

## Tools
- Databricks Lakehouse Monitoring (profile + drift tables per window, baseline table support) (gated: unconfirmed, source is paywalled or blocked).
- Elementary (`column_anomalies`, `all_columns_anomalies` dbt tests; both listed in the Elementary docs), Soda (anomaly detection, distribution checks), Monte Carlo field health (gated: unconfirmed, source is paywalled or blocked), Great Expectations (`expect_column_kl_divergence_to_be_less_than`, quantile expectations), Evidently for ML features.

## Alert tuning
- Monitor only critical columns at first (keys, amounts, statuses, ML features); all-column drift on wide tables floods alerts.
- Require persistence (2 consecutive periods) for moderate drift; page only on severe.
- Every alert should show: metric, baseline, current, top changed categories, and lineage to upstream.

## Verify
- [ ] Synthetic test (multiply a column by 100 in staging) triggers a drift alert.
- [ ] False-positive rate reviewed monthly; thresholds adjusted and documented.
