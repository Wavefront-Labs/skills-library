---
id: computing-software.data-engineering.dbt.conversion-metrics
name: conversion-metrics
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, conversion-metrics, metricflow, funnel-analysis, semantic-layer]
level: advanced
status: docs-checked
description: "Define MetricFlow conversion metrics (visit to purchase within N days): base and conversion measures, entity, window, constant properties and calculation types."
sources:
  - https://docs.getdbt.com/docs/build/conversion-metrics
  - https://docs.getdbt.com/docs/build/metrics-overview
  - https://docs.getdbt.com/docs/build/metricflow-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversion metrics

**Goal:** funnel rates such as "share of users who purchase within 7 days of visiting", computed consistently by MetricFlow.

## Definition
```yaml
metrics:
  - name: visit_to_buy_rate_7d
    label: Visit to purchase (7d)
    type: conversion
    type_params:
      conversion_type_params:
        entity: user
        calculation: conversion_rate     # or conversions (count)
        base_measure:
          name: visits
          fill_nulls_with: 0
        conversion_measure:
          name: purchases
          fill_nulls_with: 0
        window: 7 days
        constant_properties:
          - base_property: product_id
            conversion_property: product_id
```
- `base_measure` and `conversion_measure` come from semantic models that share the `entity` used to join the two events.
- A conversion is counted when the same entity has a conversion event within `window` of a base event; `constant_properties` hold a dimension or entity constant between the two events.
- `window` defaults to infinity when omitted.

## Semantics to know
- Conversions are linked to the closest preceding base event (the docs describe this with `first_value` ordered by base event date descending).
- `calculation` is `conversion_rate` (default) or `conversions`.
- `conversion_rate` is conversions divided by base events (buys/visits).

## Query
```bash
mf query --metrics visit_to_buy_rate_7d --group-by metric_time__week   # self-hosted MetricFlow; dbt platform: dbt sl query
```

## Gotchas
- The conversion is computed with a join of base and conversion events on the entity and time window, so keep event tables well organised by entity and time.

## Verify
For a small date range, compare with a hand-written SQL that joins visits to the first purchase within 7 days per user.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt conversion metrics page and MetricFlow commands page: `conversion_type_params` with `entity`, `calculation` (conversion_rate default or conversions), `base_measure`/`conversion_measure` with `fill_nulls_with`, `window` (default infinity), `constant_properties` with `base_property`/`conversion_property`, closest-base-event matching, and `mf query --metrics ... --group-by metric_time__week` (dbt sl query on the dbt platform). The page also documents a newer dbt 1.12 syntax that uses `base_metric` and `conversion_metric` instead of measures; this skill shows the measure-based form. Removed unconfirmed claims about dimension origin and event-count measures.

Method: documentation only; no commands were run.
