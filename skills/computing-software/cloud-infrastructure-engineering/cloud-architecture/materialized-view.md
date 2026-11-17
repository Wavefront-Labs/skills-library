---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.materialized-view
name: materialized-view
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, materialized-view, precomputed-views, denormalisation, refresh-materialized-view, incremental-refresh, nosql-query-patterns, change-feed]
level: practitioner
status: docs-checked
description: "Precompute query-shaped data when the source store can't answer efficiently: native vs application-built views, refresh strategy, staleness, atomic swap and rebuild."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/materialized-view", "https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html", "https://cloud.google.com/bigquery/docs/materialized-views-intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Materialized view

A materialized view is a read model that persists data derived from one or more stores, shaped for a query. It is disposable: it can be fully rebuilt from source and consumers never write to it.

## Choose the mechanism
| Mechanism | Notes (from the docs) |
|---|---|
| PostgreSQL `CREATE MATERIALIZED VIEW` | `REFRESH MATERIALIZED VIEW` replaces the whole contents. Plain refresh may block readers; `CONCURRENTLY` does not lock out selects but needs at least one UNIQUE index on column names only (no expression index, no WHERE clause) and an already-populated view. Only one refresh at a time per view. A defining `ORDER BY` is not preserved by refresh. |
| BigQuery materialized views | Refreshed in the background with incremental changes from base tables; query results are fresh because BigQuery reads the base-table changes not yet merged. Incremental views support a limited SQL subset; non-incremental views (`allow_non_incremental_definition = true`) support most queries but rerun the full query on every refresh and are not always fresh. `max_staleness` must be between 30 minutes and 3 days. See the page for the limits list (no nesting, restricted sources, query cannot be changed after creation). |
| Application-built (pipeline or background process) | Dedicated component or data pipeline maintains a separate store, possibly across stores; the Azure example builds a per-product sales summary table keyed by product category and product ID. Cosmos DB change feed consumers can maintain views. |

## Steps
1. Write down the query and the acceptable staleness before choosing a refresh model: event-driven, scheduled, external trigger or manual. The staleness window follows from refresh interval or event lag.
2. Decide full rebuild or incremental, and whether refresh blocks reads (stale results, merged results, or last complete version until refresh finishes).
3. Shape the view for the query, including computed columns; index it if the store supports it, accepting extra refresh cost.
4. Publish atomically or by versioned replacement: keep serving the last complete view while the new one is built and validated, then swap.
5. Monitor refresh recency; a lost or delayed refresh signal makes the view silently stale.

## Gotchas
- Views are tailored to one or a few queries; many queries can mean unacceptable storage cost.
- Frequent event-driven refresh on fast-changing data, or full rebuilds of large views, can dominate compute cost.
- Not suitable when source data is simple, changes very quickly, or consistency is a high priority.
- Access control: a view meant to hide data must enforce the same or stricter access than the source, and the pipeline must exclude unintended rows and columns.
- Apply the source's retention and deletion rules to every view.
- Keep view definitions in source control and CI/CD to avoid drift between environments.
- With event sourcing, views are typically necessary because the event store is hard to query directly.

## Verify
- [ ] The query uses the view and meets its latency target.
- [ ] Staleness is measured and inside the agreed window.
- [ ] A rebuild from source is scripted and timed, and a failed refresh leaves the last complete view serving.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Materialized View pattern (last updated 2026-09-25); PostgreSQL current docs, REFRESH MATERIALIZED VIEW; BigQuery, Introduction to materialized views (updated 2026-10-26).
Removed as unconfirmed: Snowflake and Redshift behaviour, DynamoDB GSI as a materialized view, reconciliation-job advice, `refreshed_at` column convention and the "refresh time approaches interval" threshold.
Method: documentation only; no commands were run.
