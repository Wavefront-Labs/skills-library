---
id: computing-software.database-administration.time-series-databases.questdb-designated-timestamp-partitions
name: questdb-designated-timestamp-partitions
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-questdb, questdb-designated-timestamp-partitions, questdb]
level: practitioner
status: draft
description: "Create QuestDB tables partitioned by time for fast ingest and retention."
sources:
  - https://questdb.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designated timestamp and partitions

**Goal:** Create QuestDB tables partitioned by time for fast ingest and retention.

## Steps
```
CREATE TABLE readings (ts TIMESTAMP, device SYMBOL, temp DOUBLE)
TIMESTAMP(ts) PARTITION BY DAY WAL;
```
- `TIMESTAMP(ts)` designates the time column; required for time-series features such as `SAMPLE BY`, ASOF JOIN, and partitioning.
- Partition by HOUR, DAY, MONTH or YEAR; pick so partitions are hundreds of MB.
- `SYMBOL` columns are dictionary-encoded strings for repeated values (add `INDEX` if filtered often).
- `WAL` tables allow concurrent writers and out-of-order data.
- Retention: `ALTER TABLE readings DROP PARTITION WHERE ts < dateadd('d', -30, now());` or TTL clauses in newer versions (confirm).
- Query: `SELECT ts, avg(temp) FROM readings SAMPLE BY 5m FILL(PREV);`.

**Gotcha:** Choosing monthly partitions for high-volume tables makes partition drops coarse and queries touch large files.

## Verify
- `SHOW PARTITIONS FROM readings;` lists the expected partitions.
- `SAMPLE BY` returns regular buckets.
