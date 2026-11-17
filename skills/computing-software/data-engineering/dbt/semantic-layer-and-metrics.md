---
id: computing-software.data-engineering.dbt.semantic-layer-and-metrics
name: semantic-layer-and-metrics
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-semantic-layer, metricflow, semantic-model, metrics, entities, dimensions, measures, metric-tree, derived-metrics, headless-bi, kpi-consistency]
level: advanced
status: docs-checked
description: "Define dbt Semantic Layer / MetricFlow semantic models and metrics so the same KPI definition serves every BI tool consistently."
sources:
  - https://docs.getdbt.com/docs/build/about-metricflow
  - https://docs.getdbt.com/docs/build/metrics-overview
  - https://docs.getdbt.com/docs/build/semantic-models
  - https://docs.getdbt.com/docs/build/ratio-metrics
  - https://docs.getdbt.com/docs/build/derived-metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt Semantic Layer / MetricFlow — one metric definition, every BI tool

**Goal:** stop "revenue" meaning something slightly different in Looker, Tableau, and the ad hoc analyst query that fed last quarter's board deck — define it once, query it everywhere.

## 1. The problem this actually solves
Without a semantic layer, each BI tool re-implements business logic independently, so "active customer" or "net revenue" can be defined several slightly different ways. The dbt Semantic Layer defines metrics once, on top of dbt models, with MetricFlow generating the SQL, so the definition lives with the data model rather than in each BI tool's config.

## 2. Semantic models — the layer between dbt models and metrics
```yaml
semantic_models:
  - name: orders
    model: ref('fct_orders')
    defaults: {agg_time_dimension: order_date}
    entities:
      - {name: order_id, type: primary}
      - {name: customer_id, type: foreign}
    dimensions:
      - {name: order_date, type: time, type_params: {time_granularity: day}}
      - {name: status, type: categorical}
    measures:
      - {name: order_total, agg: sum, expr: amount}
      - {name: order_count, agg: count}
```
A semantic model wraps one dbt model and declares its **entities** (join keys, with a `type` such as primary, foreign or unique), **dimensions** (things to group/filter by, categorical or time) and **measures** (aggregations, each with a required `agg`). `agg_time_dimension` is required when the model contains measures. MetricFlow uses entities to work out how to join semantic models when a query spans more than one, so check each entity type against the real key.

## 3. Metrics — built from measures, not redefined per tool
```yaml
metrics:
  - name: net_revenue
    type: simple
    type_params: {measure: order_total}
    filter: "{{ Dimension('order__status') }} != 'cancelled'"
  - name: order_total_metric
    type: simple
    type_params: {measure: order_total}
  - name: order_count_metric
    type: simple
    type_params: {measure: order_count}
  - name: aov
    type: ratio
    type_params: {numerator: order_total_metric, denominator: order_count_metric}
  - name: revenue_growth
    type: derived
    type_params:
      expr: "(current_revenue - prior_revenue) / prior_revenue"
      metrics: [{name: net_revenue, alias: current_revenue}, {name: net_revenue, alias: prior_revenue, offset_window: 1 month}]
```
- **Simple**: one measure, optionally filtered.
- **Ratio**: a `numerator` and `denominator`, each the name of a metric (or a dict of properties), so define the underlying simple metrics first.
- **Derived**: an `expr` over other metrics; entries can carry an `alias`, `filter` or `offset_window` (for example `1 month`) for period comparisons.
- **Cumulative**: running totals over a window.
Querying a metric grouped by a dimension from a different semantic model works when the entities connecting them are declared correctly.

## 4. Where it fits vs plain dbt models
This is not a replacement for building dimensional marts — semantic models sit on top of already-modeled dbt tables (typically marts-layer fact/dimension tables), adding a metrics/query layer, not a modeling layer. Skipping straight to semantic models without solid underlying marts just means MetricFlow is joining poorly-modeled tables instead of well-modeled ones — fix the mart layer's grain and conformance (see computing-software.data-engineering.data-modelling.dimensional-modelling-and-scd and .grain-and-fact-table-design) first.

## 5. Adoption reality check
The Semantic Layer earns its setup cost specifically when **multiple BI tools or many ad hoc query surfaces** need the same metric definitions kept consistent — a single-BI-tool shop that's disciplined about one LookML/Tableau-layer definition may not need a second semantic layer duplicating that discipline. Evaluate the actual multi-tool/multi-consumer need before adopting it as a default architecture layer.

## Verify
- [ ] Every semantic model's entity types (primary/foreign/unique) were checked against the actual join keys, not guessed — a sample cross-semantic-model query was run and its join verified against hand-written SQL.
- [ ] A ratio metric was checked to confirm it computes the ratio at the correct grain, not sum-then-divide at a coarser grain by accident.
- [ ] At least two different consumers (two BI tools, or a BI tool plus an ad hoc query) were confirmed to return identical values for the same metric and filters.
- [ ] Underlying mart-layer grain and conformed dimensions were solid before semantic models were layered on top.

## Checked
2026-11-01. Confirmed against the dbt docs repo (docs.getdbt.com): semantic model fields (entities with primary/foreign types, dimensions, measures with `agg`, `agg_time_dimension` required with measures), ratio metric `numerator`/`denominator` taking metric names, derived metric `expr`, `alias`, `offset_window`. Fixed: ratio example used measures instead of metrics. Removed: BI-tool and JDBC claims, "prevents the grain bug structurally" claim, and the automatic join-inference overstatement.
Method: documentation only; no commands were run.
