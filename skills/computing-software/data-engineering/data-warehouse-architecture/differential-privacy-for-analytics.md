---
id: computing-software.data-engineering.data-warehouse-architecture.differential-privacy-for-analytics
name: differential-privacy-for-analytics
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, differential-privacy, privacy-engineering, anonymisation, aggregation]
level: sme
status: verified
description: "Apply differential privacy to analytics outputs: epsilon and privacy budgets, contribution bounding, noisy aggregates in BigQuery and OpenDP, and when DP is warranted."
sources:
  - https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax
  - https://docs.opendp.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Differential privacy for analytics

**Goal:** publish aggregate statistics (to partners, the public, or broad internal audiences) with a mathematical bound on what can be learned about any individual.

## Core ideas
- A DP mechanism adds calibrated random noise so the output barely changes whether or not one person's data is included.
- **Epsilon (ε)**: privacy loss parameter; smaller = more private, noisier. Published deployments use a wide range of values; choose with privacy/legal stakeholders (BigQuery's own docs example uses epsilon = 10, delta = .01 only to illustrate the syntax).
- **Delta (δ)**: small probability of exceeding the bound (approximate DP), much smaller than 1/number of users.
- **Privacy budget**: each query spends ε; repeated queries on the same data add up (composition). Track the budget per dataset/audience.
- **Contribution bounding**: limit how many rows and how large a value one user can contribute; sensitivity (and noise scale) depends on these bounds.

## BigQuery
```sql
SELECT WITH DIFFERENTIAL_PRIVACY
  OPTIONS (epsilon = 1.0, delta = 1e-6, max_groups_contributed = 1, privacy_unit_column = user_id)
  country,
  AVG(order_value, contribution_bounds_per_group => (0, 500)) AS avg_order,
  COUNT(*) AS orders
FROM sales.orders
GROUP BY country;
```
Groups with few contributors can be dropped by the noisy thresholding: BigQuery's docs example notes a group "was removed this time, but might not be removed the next time". The clause is `WITH DIFFERENTIAL_PRIVACY OPTIONS(epsilon, delta, [max_groups_contributed], privacy_unit_column)`; per its syntax `max_groups_contributed` is optional and the other three are listed as required. The query was not run (no BigQuery account); syntax is from the BigQuery reference.

## OpenDP (Python)
Library for building DP pipelines: clamp values, bound contributions, apply Laplace/Gaussian mechanisms, account for budget across queries. Ran with `opendp` 0.16.0 (`dp.enable_features("contrib")`): `space >> dp.t.then_clamp((0., 500.)) >> dp.t.then_sum() >> dp.m.then_laplace(scale=500.)` over a `dp.vector_domain(dp.atom_domain(T=float, nan=False))` with `dp.symmetric_distance()` returned a noisy sum, and `meas.map(1)` gave epsilon of about 1.0 (the privacy loss for scale = sensitivity).

## Where it fits
- Public/open data releases, cross-company sharing (clean rooms often offer DP options), broad dashboards over sensitive populations.
- Not needed for small trusted analyst groups with access controls; k-anonymity/aggregation thresholds are weaker but simpler and often adequate internally.

## Gotchas
- Noise hurts small groups most: plan coarser groupings for DP outputs.
- Joins and pre-processing before DP can break the contribution bounds if users appear in multiple rows; define the privacy unit carefully.
- Rerunning a DP query to "get better numbers" spends budget and can leak.

## Verify
Utility check: DP outputs vs true values on historical data within acceptable error for intended uses; budget ledger records every release.
