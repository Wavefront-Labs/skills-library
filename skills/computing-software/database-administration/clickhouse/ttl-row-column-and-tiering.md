---
id: computing-software.database-administration.clickhouse.ttl-row-column-and-tiering
name: ttl-row-column-and-tiering
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, ttl, delete-where, group-by-ttl, merge-with-ttl-timeout]
level: practitioner
status: docs-checked
description: "Expire, roll up or move ClickHouse data with column and row TTL, rollup GROUP BY TTL and TO VOLUME tiering, with merge timing."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/ttl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ttl row column and tiering
TTL moves, deletes or rolls up rows or columns after an interval; it applies to whole tables or specific columns. The INTERVAL is added to a Date or DateTime value.
```sql
-- column TTL: on expiry the value is replaced by the type's default
CREATE TABLE example1 (
   timestamp DateTime,
   x UInt32 TTL timestamp + INTERVAL 1 MONTH,
   y String TTL timestamp + INTERVAL 1 DAY,
   z String
)
ENGINE = MergeTree
ORDER BY tuple()

-- row TTL with a condition; multiple conditions allowed
CREATE TABLE events (`event` String, `time` DateTime, `value` UInt64)
ENGINE = MergeTree
ORDER BY (event, time)
TTL time + INTERVAL 1 MONTH DELETE WHERE event != 'error',
    time + INTERVAL 6 MONTH DELETE WHERE event = 'error'

-- add column TTLs to an existing table
ALTER TABLE customers
MODIFY COLUMN balance Int32 TTL timestamp + INTERVAL 2 HOUR,
MODIFY COLUMN address String TTL timestamp + INTERVAL 2 HOUR
```
If all values of a column in a part expire, ClickHouse deletes that column from the part on the filesystem.

Rollup: add `GROUP BY` to the TTL and columns to hold results.
```sql
CREATE TABLE hits (
   timestamp DateTime, id String, hits Int32,
   max_hits Int32 DEFAULT hits,
   sum_hits Int64 DEFAULT hits
)
ENGINE = MergeTree
PRIMARY KEY (id, toStartOfDay(timestamp), timestamp)
TTL timestamp + INTERVAL 1 DAY
    GROUP BY id, toStartOfDay(timestamp)
    SET max_hits = max(max_hits), sum_hits = sum(sum_hits);
```
The GROUP BY columns must be a prefix of the PRIMARY KEY, and the defaults of the result columns must be `hits` for the logic to work.

Tiering (not applicable to ClickHouse Cloud): define disks and volumes under `storage_configuration` in a file in `/etc/clickhouse-server/config.d/`, then:
```sql
ALTER TABLE my_table
   MODIFY TTL
      trade_date TO VOLUME 'hot_volume',
      trade_date + INTERVAL 2 YEAR TO VOLUME 'warm_volume',
      trade_date + INTERVAL 4 YEAR TO VOLUME 'cold_volume';
ALTER TABLE my_table MATERIALIZE TTL
```
`TO DISK` and `TO VOLUME` name disks or volumes from the configuration. `system.disks` and `system.storage_policies` list them, and `system.parts` (`disk_name`) shows where parts are.

Timing: expiry happens only during merges. `merge_with_ttl_timeout` (minimum delay in seconds before repeating a merge with delete TTL) and `merge_with_recompression_ttl_timeout` both default to 14400 seconds (4 hours). `OPTIMIZE TABLE example1 FINAL` forces a merge, but the docs do not recommend it frequently.

Best practice: for table-level row TTL partition by the date or month of the same time field, so whole partitions can be dropped instead of rewriting parts: `toYYYYMMDD(date_field)` for TTLs of days or weeks, `toYYYYMM(date_field)` or `toStartOfMonth(date_field)` for months or years.

## Checked
2026-11-03. Confirmed against the "Manage data with TTL" page. Removed: the invented `TO DISK 'cold'` example (the page's example uses `TO VOLUME`), the claim that expired rows may be returned until a merge (the page only says deletion and aggregation are not immediate), and the system.parts min_time/max_time Verify query.
Method: documentation only; no commands were run.
