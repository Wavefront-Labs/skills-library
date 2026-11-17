---
id: computing-software.data-engineering.data-warehouse-architecture.data-apis-and-low-latency-serving
name: data-apis-and-low-latency-serving
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-serving, data-api, serving-store, key-value-store, caching, pagination, api-design, postgres-serving, customer-facing-analytics]
level: practitioner
status: docs-checked
description: "Expose curated data to applications via APIs: why not to query the warehouse per request, choosing a serving store, loading it, endpoint and pagination design, and caching."
sources:
  - https://cloud.google.com/bigquery/quotas
  - https://docs.snowflake.com/en/user-guide/tables-hybrid
  - https://www.postgresql.org/docs/current/sql-copy.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
  - https://google.aip.dev/158
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data APIs and low-latency serving stores

**Goal:** applications get curated data (customer metrics, recommendations, account summaries) in milliseconds at high concurrency, without turning the warehouse into an OLTP database.

## 1. Don't serve from the warehouse directly (usually)
Warehouses are tuned for scans and aggregation, not thousands of point lookups per second. BigQuery enforces project limits on interactive queries (for example, up to 1,000 queued interactive queries; extra ones return a quota error), and Snowflake notes that standard tables give better performance on large analytical queries.
Exceptions: internal tools with low QPS, and engines built for it. Snowflake hybrid tables use a row store with row-level locking and enforced primary keys, suit index-based random point reads and high-concurrency writes, and Snowflake lists "lower-latency serving of precomputed aggregates through an API" as a use case. They typically have a larger storage footprint than standard tables.

## 2. Choose the serving store by access pattern (design guidance)
| Access pattern | Store |
|---|---|
| Get by key (customer_id to profile/metrics) | DynamoDB, Bigtable, Redis, Cassandra |
| Filtered lists, small joins, moderate QPS | Postgres / MySQL (read replicas), or a Snowflake hybrid table |
| Aggregations over fresh events, user-facing dashboards | ClickHouse / Pinot / Druid |
| Full-text / faceted search | OpenSearch / Elasticsearch |
| Vector similarity | pgvector, a vector DB |
For DynamoDB, design partition keys, sort keys and secondary indexes around the access pattern; its best-practices guide has sections on each, on bulk data operations and on DAX caching.

## 3. Load the store from the warehouse
- Batch: export the curated table, bulk load into a new table, then swap so readers never see half-loaded data (design guidance).
```sql
BEGIN;
ALTER TABLE customer_metrics RENAME TO customer_metrics_old;
ALTER TABLE customer_metrics_new RENAME TO customer_metrics;
COMMIT;
DROP TABLE customer_metrics_old;
```
- Postgres bulk load: `COPY customer_metrics_new FROM STDIN WITH (FORMAT csv)`. COPY moves data between tables and files or STDIN; the binary format is somewhat faster than text and CSV but less portable across architectures and versions.
- Key-value: idempotent batch writes with retry of unprocessed items; see the store's bulk operations guidance.
- Incremental: CDC or a stream of changed rows when freshness matters.

## 4. API design
- Resource-oriented endpoints: `GET /v1/customers/{id}/metrics`.
- Paginate from the start: Google AIP-158 says adding pagination to an existing method is backwards-incompatible. Use `page_size` (optional; API picks and documents a default, coerces values above its maximum down, errors on negative values) and `page_token`, with `next_page_token` empty only at the end of the collection.
- Page tokens must be opaque, URL-safe strings (base-64 of a readable token is not enough), must carry no authorization (check authorisation on every request), and callers must keep other arguments the same between pages.
- Keyset pagination (token encodes the last key) rather than OFFSET is design guidance, not an AIP-158 requirement.
- Return an `as_of` freshness timestamp so consumers know how current the data is.
- Version the API; data model changes in the warehouse must not leak straight into responses.
- Auth per consumer, rate limits, and tenant row-level filtering in the API layer.

## 5. Caching and SLOs (design guidance)
- Cache hot keys (CDN for public aggregates, Redis for per-user) with TTL aligned to the load cadence; invalidate on swap.
- SLOs: p99 latency, availability, freshness (max data age). Alert on all three.

## Verify
- [ ] p99 latency and QPS measured with a load test at expected peak.
- [ ] Loads swap atomically; no partial data visible during refresh.
- [ ] Responses include data freshness; freshness SLO alerting exists.

## Checked
Date: 2026-11-09. Confirmed from the Snowflake hybrid tables page (read in full), Google AIP-158 (read in full), the BigQuery quotas page (searched for interactive query limits) and the PostgreSQL COPY page (searched). The DynamoDB page is only a topic index, so its BatchWriteItem 25-item limit was removed. Removed as unconfirmed: "100 ms-seconds" latency, "orders of magnitude faster" COPY, build-indexes-after-load, Databricks online tables. Sections marked design guidance are not page claims.
Method: documentation only; no commands were run.
