---
id: computing-software.database-administration.time-series-databases.clickhouse-ttl-materialized-views
name: clickhouse-ttl-materialized-views
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-clickhouse, clickhouse-ttl-materialized-views, clickhouse]
level: practitioner
status: draft
description: "Expire data and keep rollups automatically in ClickHouse."
sources:
  - https://clickhouse.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TTL and materialized views

**Goal:** Expire data and keep rollups automatically in ClickHouse.

## Steps
- Row TTL: `ALTER TABLE metrics MODIFY TTL ts + INTERVAL 90 DAY;` expired parts are dropped in background merges (`ttl_only_drop_parts = 1` makes it cheap).
- Move to cold storage: `TTL ts + INTERVAL 7 DAY TO VOLUME 'cold'`.
- Rollup via materialized view into `AggregatingMergeTree`: `CREATE MATERIALIZED VIEW m_5m TO metrics_5m AS SELECT toStartOfFiveMinutes(ts) AS ts, series_id, avgState(value) AS v FROM metrics GROUP BY ts, series_id;`.
- Read rollups with `avgMerge(v)`; store `sumState`/`countState` for re-aggregation.
- Materialized views only see data inserted after creation; backfill with `INSERT INTO metrics_5m SELECT ...`.
- Late data lands in the right group because merge combines states.

**Gotcha:** A materialized view processes each insert block alone, so it cannot join or see earlier rows; do aggregation via States only.

## Verify
- Rollup totals equal raw totals for a closed window.
- `system.parts` shows expired partitions disappearing.
