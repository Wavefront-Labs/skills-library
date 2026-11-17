---
id: computing-software.data-engineering.dbt.saved-queries-and-exports
name: saved-queries-and-exports
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-semantic-layer, metricflow, saved-queries, exports, mf-query, semantic-layer-apis, jdbc-graphql, metric-caching]
level: advanced
status: docs-checked
description: "Query and publish dbt Semantic Layer metrics: mf/dbt sl query CLI, saved queries in YAML, exports that write tables/views on schedule, and API access from BI tools."
sources:
  - https://docs.getdbt.com/docs/build/saved-queries
  - https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports
  - https://docs.getdbt.com/docs/build/metricflow-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saved queries, exports and querying metrics

**Goal:** consumers get consistent metric results whether they query interactively, through a BI tool, or from a published table.

## Query from the CLI
```bash
# dbt Core with MetricFlow installed (pip install dbt-metricflow)
mf query --metrics net_revenue,orders --group-by metric_time__week,customer__segment \
  --where "{{ Dimension('customer__region') }} = 'EMEA'" --start-time 2026-01-01 --order-by -metric_time__week
mf query --metrics net_revenue --group-by metric_time__month --explain     # show generated SQL
# dbt Cloud CLI
dbt sl query --metrics net_revenue --group-by metric_time__month
```

## Saved queries
```yaml
saved_queries:
  - name: weekly_revenue_by_segment
    description: Canonical weekly revenue cut used by finance.
    query_params:
      metrics: [net_revenue, orders]
      group_by:
        - TimeDimension('metric_time', 'week')
        - Dimension('customer__segment')
      where:
        - "{{ Dimension('customer__region') }} = 'EMEA'"
    exports:
      - name: weekly_revenue_by_segment
        config:
          export_as: table          # or view
          schema: metrics_exports
```
Saved queries give named, reusable metric queries. An `export_as` set on the saved query is inherited by its exports unless the export config sets its own.

## Exports
Exports run saved queries and write the output to a table or view in your data platform using the dbt job scheduler. Use them for tools that do not natively support the Semantic Layer, or to pre-populate the cache for the Semantic Layer APIs. Running an export counts towards queried metrics usage; querying the resulting table or view does not.

## APIs
The Semantic Layer APIs serve metrics dynamically; check the dbt docs for the current APIs and integrations.

## Gotchas
- Dimension references use entity paths (`customer__segment`); typos error at query time: validate configs in CI (`dbt sl validate` / `mf validate-configs`).
- Exported tables are snapshots: freshness = last export run.

## Checked
2026-11-01. Confirmed against the dbt saved queries, exports and MetricFlow commands pages: `dbt sl` (dbt platform) and `mf` (self-hosted) prefixes, `dbt sl validate` and `mf validate-configs`, `export_as` inheritance, exports writing a table or view via the job scheduler, export versus query usage. Removed: API protocol and BI tool list, service token claim, `dbt build` validating saved queries, export ordering claim.
Method: documentation only; no commands were run.

## Verify
- [ ] `--explain` SQL for a key metric matches the hand-written reference query result.
- [ ] Export table refreshes in the scheduled job and BI points at it (or at the API), not at ad-hoc SQL.
