---
id: computing-software.data-engineering.etl-pipeline-design.query-based-cdc-and-its-limits
name: query-based-cdc-and-its-limits
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, query-based-cdc, updated-at-polling, incremental-extraction, watermarks]
level: practitioner
status: docs-checked
description: "Implement query-based CDC by polling updated_at or rowversion columns safely: overlap windows, transaction visibility gaps, deletes, and when to move to log-based CDC."
sources:
  - https://debezium.io/blog/2018/07/19/advantages-of-log-based-change-data-capture/
  - https://docs.confluent.io/kafka-connectors/jdbc/current/source-connector/overview.html#incremental-query-modes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query-based CDC (updated_at polling) and its limits

**Goal:** incremental extraction from a database where log-based CDC is not available, without silently missing rows.

## Basic pattern
```sql
select * from orders
where updated_at > :last_watermark - interval '10 minutes'   -- overlap
  and updated_at <= :run_upper_bound                          -- fixed upper bound for the run
order by updated_at;
```
- Save `:run_upper_bound` (taken at run start, minus a safety lag) as the next watermark, not `max(updated_at)` of fetched rows only.
- Load with **merge on primary key** so overlap rows are deduplicated.
- Prefer an `updated_at` maintained by the database (trigger or default) over one set by the application.

## Known failure modes
1. **Long transactions**: a row updated at 10:00 commits at 10:15; a run at 10:05 with upper bound 10:05 does not see it; next run starts at 10:05 minus overlap and might miss it if overlap < transaction duration. Mitigate with overlap windows larger than the longest transaction, or upper bound = now minus max transaction time.
2. **updated_at not maintained** by bulk updates, admin scripts or replication: rows never re-extracted. Test it; add a DB trigger if needed.
3. **Hard deletes are invisible**. Options: soft delete flags in the source, periodic full key comparison (extract all PKs and anti-join), or trigger-written delete log.
4. **Clock/time zone issues**: compare in the DB's own clock and time zone.
5. **Load on the source**: index `updated_at`; query replicas.

## Kafka Connect JDBC source
`mode=timestamp+incrementing` with `timestamp.column.name` and `incrementing.column.name`. Set `timestamp.delay.interval.ms` larger than the longest write transaction on the source tables, so rows that commit late are not skipped.

## When to switch to log-based CDC
Need deletes, intermediate states, sub-minute latency, or very large tables where polling scans hurt: use Debezium/DMS/Datastream on the transaction log.

## Verify
Weekly reconciliation: count and checksum of rows by updated_at day, source vs target; key comparison finds deletes.

## Checked

2026-10-28. Confirmed in the Confluent JDBC source connector page: `mode=timestamp+incrementing` with `timestamp.column.name` and `incrementing.column.name`, and `timestamp.delay.interval.ms` sized above the longest write transaction. Removed: the `rowversion` and Postgres `xmin` wraparound claims (not in the cited pages). The remaining text is design reasoning with no figures.

Method: documentation only; no commands were run.
