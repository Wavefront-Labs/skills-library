---
id: computing-software.database-administration.sqlite.analyze-sqlite-stat1-and-pragma-optimize
name: analyze-sqlite-stat1-and-pragma-optimize
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-query-planner, sqlite-stat1, analyze, pragma-optimize, sqlite-stat4, analysis-limit, query-planner-stability]
level: practitioner
status: verified
description: "Give the SQLite query planner real statistics with ANALYZE, sqlite_stat1/stat4 and PRAGMA optimize, and keep plans stable in shipped apps."
sources:
  - https://www.sqlite.org/lang_analyze.html
  - https://www.sqlite.org/pragma.html#pragma_optimize
  - https://www.sqlite.org/queryplanner-ng.html#howtofix
  - https://www.sqlite.org/fileformat2.html#stat1tab
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ANALYZE, sqlite_stat1 and PRAGMA optimize

**Goal:** the planner picks the right index on skewed data, without running a full ANALYZE on every app launch.

## What ANALYZE stores
```sql
ANALYZE;                       -- whole database
ANALYZE main.orders;           -- one table
SELECT * FROM sqlite_stat1;    -- tbl | idx | stat  e.g. "orders|idx_orders_status|250000 62500"
```
`stat` = row count, then average rows per distinct value for each index prefix column (run on SQLite 3.50.4: 2000 rows, 2 distinct statuses gave `2000 1000`). Without stats SQLite falls back on built-in default estimates and may choose a poor index.
`sqlite_stat4` (needs the `SQLITE_ENABLE_STAT4` compile option, off in the Python 3.14 build tested) adds histogram data. A non-zero `analysis_limit` skips it.

## PRAGMA optimize (recommended routine)
```sql
PRAGMA optimize;                       -- before closing each connection (or periodically)
PRAGMA optimize=0x10002;               -- long-lived connections, right after opening: 0x10000 checks all tables + 0x2 runs ANALYZE where useful
PRAGMA analysis_limit=1000;            -- docs suggest 100 or 1000: approximate ANALYZE
```
`optimize` reruns ANALYZE only on tables whose row counts changed a lot or that queries showed would benefit; usually a no-op and cheap.

## Large or embedded deployments
- Long-running apps: `PRAGMA optimize=0x10002` on open, then `PRAGMA optimize` periodically (docs: perhaps once per day or hour); short-lived connections run it once just before closing; run it after schema changes, especially CREATE INDEX. Since 3.46.0 optimize limits ANALYZE scope itself.
- With `analysis_limit` of 100-1000, ANALYZE runs quickly even on enormous files (results are approximate but usually good enough).
- Stability: run ANALYZE only in development, export `sqlite_stat1` as SQL (script on the lang_analyze page), replay it at database creation, then `ANALYZE sqlite_schema` to reload; do not run ANALYZE or `PRAGMA optimize` in the shipped app if plans must stay frozen.

## Checking the effect
```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'open' AND created_at > '2026-10-01';
```
Compare before/after ANALYZE. `.expert` in the sqlite3 shell suggests indexes.

## Gotchas
- Stats are not updated as data changes: rerun ANALYZE (or optimize) after big imports or schema changes.

## Verify
`SELECT count(*) FROM sqlite_stat1` > 0 and the problem query's `EXPLAIN QUERY PLAN` shows `SEARCH ... USING INDEX` with the selective index.
