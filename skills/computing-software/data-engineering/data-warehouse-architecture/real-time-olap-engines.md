---
id: computing-software.data-engineering.data-warehouse-architecture.real-time-olap-engines
name: real-time-olap-engines
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-serving, real-time-olap, clickhouse, apache-druid, apache-pinot, mergetree, kafka-ingestion, user-facing-analytics, rollups]
level: practitioner
status: docs-checked
description: "Use ClickHouse, Druid or Pinot for sub-second analytics on fresh events: when to choose each, ClickHouse MergeTree design, Kafka ingestion, rollups and upserts."
sources:
  - https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
  - https://clickhouse.com/docs/engines/table-engines/integrations/kafka
  - https://clickhouse.com/docs/materialized-view/incremental-materialized-view
  - https://druid.apache.org/docs/latest/design/
  - https://docs.pinot.apache.org/basics/concepts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Real-time OLAP (ClickHouse / Druid / Pinot)

**Goal:** aggregate queries over billions of recent events in well under a second, at user-facing concurrency, seconds after the event happened.

## 1. When to use one
- User-facing analytics (in-product dashboards), observability, ad-tech/clickstream, with high QPS and freshness of seconds.
- Not a replacement for the warehouse: denormalise before loading and test your join patterns.

## 2. Choosing
| | ClickHouse | Apache Druid | Apache Pinot |
|---|---|---|---|
| Strength | general-purpose SQL, fast scans | rollup at ingestion | see the Pinot concepts docs |
| Ingest | Kafka table engine, INSERT batches | see the Druid ingestion docs | see the Pinot docs |
| Updates | ReplacingMergeTree | see the Druid docs | see the Pinot docs |

## 3. ClickHouse table design
```sql
CREATE TABLE events (
  event_time DateTime64(3), tenant_id UInt32, user_id UInt64,
  event_type LowCardinality(String), amount Decimal(18,2))
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (tenant_id, event_type, event_time)
TTL toDateTime(event_time) + INTERVAL 13 MONTH;
```
- `ORDER BY` is the sparse primary index: lead with the columns every query filters on (tenant first for multi-tenant), low cardinality before high.
- Partition coarsely (month); too many partitions = too many parts = "Too many parts" errors.
- Insert in batches or enable `async_insert` (see ClickHouse's asynchronous inserts page); row-by-row inserts create many small parts.
- `LowCardinality(String)` for enum-like columns; avoid `Nullable` unless needed.

## 4. Kafka → rollup pipeline in ClickHouse
```sql
CREATE TABLE events_queue (...) ENGINE = Kafka
  SETTINGS kafka_broker_list='<broker>:9092', kafka_topic_list='events',
           kafka_group_name='ch_events', kafka_format='JSONEachRow';
CREATE MATERIALIZED VIEW events_mv TO events AS SELECT * FROM events_queue;

CREATE TABLE events_hourly (hour DateTime, tenant_id UInt32, event_type LowCardinality(String),
  n AggregateFunction(count), revenue AggregateFunction(sum, Decimal(18,2)))
ENGINE = AggregatingMergeTree ORDER BY (tenant_id, event_type, hour);
CREATE MATERIALIZED VIEW events_hourly_mv TO events_hourly AS
SELECT toStartOfHour(event_time) AS hour, tenant_id, event_type, countState() AS n, sumState(amount) AS revenue
FROM events GROUP BY hour, tenant_id, event_type;
-- query: SELECT hour, countMerge(n), sumMerge(revenue) FROM events_hourly WHERE tenant_id=7 GROUP BY hour
```
Materialized views are insert triggers: they only see new inserts, so backfill rollups explicitly with `INSERT INTO events_hourly SELECT ...`.

## 5. Upserts and dedup
- `ReplacingMergeTree(version)` deduplicates by ORDER BY key during background merges, not immediately; see the engine docs for exact-read options.
- Druid: rollup at ingestion (`queryGranularity`) trades detail for size; choose granularity per datasource.

## Verify
- [ ] p95 latency at target QPS measured with production-shaped queries.
- [ ] Ingestion lag (Kafka consumer lag) is monitored and seconds-level.
- [ ] Part count per partition stays healthy (`system.parts`), no "Too many parts" errors.

## Checked

2026-10-28. Confirmed: ClickHouse Kafka table engine settings (`kafka_broker_list`, `kafka_topic_list`, `kafka_group_name`, `kafka_format`, `JSONEachRow`), `AggregatingMergeTree` and `ReplacingMergeTree` in the MergeTree family, "too many parts", asynchronous inserts (`async_insert`); Druid rollup page: rollup at ingestion and `queryGranularity`. Removed: Pinot upsert and star-tree claims, Druid supervisor and ClickPipes claims, insert-rate figures, `FINAL`/`argMax` advice (the Pinot concepts page was nearly empty and the rest was not found).

Method: documentation only; no commands were run.
