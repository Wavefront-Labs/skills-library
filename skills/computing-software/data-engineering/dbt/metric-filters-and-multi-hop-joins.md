---
id: computing-software.data-engineering.dbt.metric-filters-and-multi-hop-joins
name: metric-filters-and-multi-hop-joins
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, metric-filters, metricflow, entities, semantic-layer]
level: advanced
status: gated
description: "Write MetricFlow metric and query filters with Dimension, TimeDimension and Entity templates, and understand entity joins, multi-hop limits and fan-out protection."
sources:
  - https://docs.getdbt.com/docs/build/ref-metrics-in-filters
  - https://docs.getdbt.com/docs/build/join-logic
  - https://docs.getdbt.com/docs/build/entities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric filters and multi-hop joins

**Goal:** filtered metrics (EMEA revenue, paid orders) and dimensions from related models without hand-written joins.

## Filter syntax
```yaml
metrics:
  - name: revenue_emea
    type: simple
    label: Revenue EMEA
    type_params:
      measure: revenue
    filter: |
      {{ Dimension('customer__region') }} = 'EMEA'
      and {{ TimeDimension('metric_time', 'day') }} >= '2026-01-01'
```
- `Dimension('<entity>__<dimension>')`: entity prefix says which semantic model it comes from.
- `TimeDimension('<name>', '<grain>')`, `Entity('<name>')`.
- Same syntax in query `where` clauses: `mf query --metrics revenue --group-by metric_time__month --where "{{ Dimension('customer__region') }} = 'EMEA'"`.
- Metric-level filters combine (AND) with query filters.

## How joins happen
MetricFlow joins semantic models through **entities** (primary/unique/foreign keys). Querying `revenue` (from orders, foreign entity `customer`) by `customer__region` joins orders to customers on the `customer` entity automatically.

## Multi-hop
Dimensions reachable through a chain (orders -> customer -> country) are reached through a multi-hop join; the join-logic page says a dimension two hops away cannot be addressed as `customer__country__region_name` and that the entity path is given as a list. See that page for syntax. Limits:
- Only joins that cannot fan out (foreign-to-primary/unique) are allowed; many-to-many is refused to protect metric correctness.
- The join-logic page says MetricFlow can join up to three tables, with a limit of two hops, and labels multi-hop joins as applying to dbt v1.12 and later; deeper paths need a denormalised dimension in an intermediate model.

## Gotchas
- Name the entity consistently across semantic models (`customer` everywhere), otherwise no join path exists.
- Filters in YAML need the `|` block and Jinja-style templates; plain column names are rejected. (gated: unconfirmed, source is paywalled or blocked)
- `mf list dimensions --metrics revenue` shows exactly which dimension names are valid.

## Verify
`mf query --explain` shows the generated SQL with the expected joins and WHERE; numbers match a hand-written query.

## Checked

2026-11-02

- Confirmed: The dbt join-logic page (fan-out joins not allowed, three-table and two-hop limits, entity__dimension naming) and the entities page were fetched.
- Removed or gated: Fixed the invented `customer__country__region` naming and the vague hop limit. Gated: the Dimension/TimeDimension/Entity template syntax and the mf commands are not shown on the fetched pages (the ref-metrics-in-filters page covers metrics as dimensions only).

Method: documentation only; no commands were run.
