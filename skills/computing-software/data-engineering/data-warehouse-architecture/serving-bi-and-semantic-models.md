---
id: computing-software.data-engineering.data-warehouse-architecture.serving-bi-and-semantic-models
name: serving-bi-and-semantic-models
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-serving, bi-serving, semantic-layer, power-bi, import-vs-directquery, aggregate-tables, bi-performance, service-accounts]
level: practitioner
status: draft
description: "Serve warehouse data to BI tools: mart shape for dashboards, import vs live/DirectQuery, a single semantic layer for metrics, aggregates, BI service accounts and cost control."
sources:
  - https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about
  - https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
  - https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl
  - https://cloud.google.com/looker/docs/what-is-lookml
  - https://help.tableau.com/current/pro/desktop/en-us/extracting_data.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serving BI and semantic models

**Goal:** dashboards that are fast, agree with each other, and don't run up an unbounded warehouse bill.

## 1. Shape marts for BI
- Star schemas (fact + conformed dimensions) for semantic-model tools (Power BI, Looker, Tableau relationships). Power BI's VertiPaq engine is designed for stars; snowflaked or one-big-table models make DAX harder and models bigger.
- One-big-table only for a single tool that cannot model joins, or for extract-based dashboards.
- Pre-compute business logic (fiscal calendars, status mappings) in the warehouse, not in each BI tool.
- Stable names: BI tools break on column renames — treat mart schemas as a contract.

## 2. Define metrics once
- Put metric definitions in one semantic layer (dbt Semantic Layer/MetricFlow, LookML, Cube, Power BI shared semantic model, AtScale) and point every dashboard at it.
- Ban metric logic in individual workbooks for certified metrics; allow it in sandbox workspaces.
- Certify/endorse datasets so users find the right one.

## 3. Import vs live query
| Mode | Pros | Cons | Use when |
|---|---|---|---|
| Import / extract (Power BI Import, Tableau extract) | sub-second, no warehouse cost per click | refresh latency, size limits, duplicate copy | most dashboards; data refreshed hourly/daily |
| Live / DirectQuery | always current, no size limit | every visual = warehouse queries; latency; concurrency cost | very large or near-real-time data |
| Composite / hybrid / aggregations | imported aggregates + DirectQuery detail | more modelling | big fact tables with mostly summary use |
Refresh imports right after the pipeline finishes (trigger refresh via API at the end of the job), not on a clock that races it.

## 4. Performance and cost on the warehouse side
- Aggregate tables or materialized views at the grain dashboards use (day × product), not raw events.
- Cluster/partition marts by the dashboard filter columns (date first).
- Dedicated BI warehouse/compute with auto-suspend and a max cluster count; set statement timeouts and resource monitors / budgets.
- Result caching (Snowflake result cache, BigQuery cached results, Databricks query caching) helps identical queries — avoid `CURRENT_TIMESTAMP` in dashboard SQL, which defeats it.

## 5. Security
- Each BI tool connects with its own service account / OAuth, least privilege, read-only on marts.
- Row-level security: implement in the warehouse (row access policies) when users query live with their own identity; in the semantic model (Power BI RLS roles) for import mode — never both inconsistently.

## Verify
- [ ] The same metric shows the same number in every certified dashboard.
- [ ] P95 dashboard load under the agreed target (e.g. 5 s).
- [ ] BI warehouse spend is attributed and capped.
- [ ] Refresh is triggered by pipeline completion.
