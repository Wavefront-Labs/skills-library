---
id: computing-software.database-administration.time-series-databases.tsdb-cardinality-budgeting
name: tsdb-cardinality-budgeting
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-cardinality, tsdb-cardinality-budgeting]
level: practitioner
status: draft
description: "Set and enforce a series budget before launching a metrics or IoT pipeline."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cardinality budgeting

**Goal:** Set and enforce a series budget before launching a metrics or IoT pipeline.

## Steps
- Series count is the product of label values that co-occur: hosts 200 x endpoints 50 x status 5 x method 4 = 200,000 series per metric.
- Write the budget per metric in a design doc: expected series, growth per month, and who owns it.
- Multiply by bucket count for Prometheus histograms (each bucket is a series); 12 buckets x 200,000 = 2.4M.
- Enforce: scrape sample limits (Prometheus), per-tenant limits (Mimir), bucket schema review (Influx), alerts on series growth rate.
- Review new labels in code review: reject unbounded values (ids, paths, emails).
- Track ratio of series to samples (churn) as well as total.

**Gotcha:** Cardinality compounds silently when someone adds one label to a metric that already has many; always recompute the product.

## Verify
- Dashboard shows series per metric against its budget.
- Alert fires when growth exceeds the budget by 20 percent.
