---
id: computing-software.database-administration.sqlite.virtual-tables-csv-series-dbstat
name: virtual-tables-csv-series-dbstat
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, virtual-table, generate-series, dbstat, csv-virtual-table, sqlite-query-planner]
level: practitioner
status: gated
description: "Use SQLite virtual tables such as generate_series, csv, dbstat and json_each for calendars, file imports and space analysis, and understand their planner interface."
sources:
  - https://sqlite.org/vtab.html
  - https://sqlite.org/series.html
  - https://sqlite.org/dbstat.html
  - https://sqlite.org/csv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual tables (csv / generate_series / dbstat)

A virtual table looks like a table but is implemented by code (a module). The planner calls the module's `xBestIndex` to learn which constraints it can use.

## generate_series (built into the 3.54.1 shell; not in the Python 3.14 module's `pragma_module_list`, so a loadable extension there)
```sql
SELECT value AS day_offset FROM generate_series(0, 6);
-- calendar of the last 30 days with zero-filled counts
SELECT date('now', '-' || value || ' days') AS day, count(o.id)
FROM generate_series(0, 29)
LEFT JOIN orders o ON date(o.created_at) = date('now', '-' || value || ' days')
GROUP BY day ORDER BY day;
```
Older shells without it: use a recursive CTE.

## csv (ext/misc/csv.c)
```text
.load ./csv
CREATE VIRTUAL TABLE temp.imp USING csv(filename='data.csv', header=yes);
SELECT * FROM temp.imp LIMIT 5;
INSERT INTO customers SELECT * FROM temp.imp;
```
Read-only (the module's `xUpdate` is null outside test builds), every query re-reads the file; copy into a real table for repeated use. (`.import --csv` in the shell is the quicker one-off.) The sqlite.org 3.54.1 shell does not include this module: `.load ./csv` needs a compiled `csv.dll`/`.so` from `ext/misc/csv.c`, and no C compiler is available here, so the `csv` example was not run (gated: unconfirmed, source is paywalled or blocked). Parameters taken from the `csv.c` header and parser: `filename=` or `data=`, `schema=`, `columns=N`, `header=YES|NO`; with neither `columns` nor `schema` the columns come from the first line.

## dbstat (space by table/index)
Requires `SQLITE_ENABLE_DBSTAT_VTAB` (the 3.54.1 shell has it; the query below ran there):
```sql
SELECT name, sum(pgsize)/1024/1024.0 AS mb, sum(unused)*100.0/sum(pgsize) AS pct_free
FROM dbstat GROUP BY name ORDER BY mb DESC LIMIT 15;
```
Finds the biggest tables/indexes and fragmentation before `VACUUM`.

## json_each / json_tree
Table-valued functions over JSON:
```sql
SELECT o.id, j.value ->> '$.sku' FROM orders o, json_each(o.items) j;
```

## Other modules
`fts5`, `rtree`, `pragma_*` functions, `sqlite_dbpage` (raw pages), `zipfile`, `fsdir`, `bytecode`, `tables_used`, `completion` (all in the 3.54.1 shell's `pragma_module_list`), and `carray` (bind arrays from C; the shell lists `ENABLE_CARRAY` in compile options).

## Gotchas
- Virtual tables may ignore constraints they cannot use; the plan shows `SCAN ... VIRTUAL TABLE INDEX n:...` (3.54.1 printed `SCAN generate_series VIRTUAL TABLE INDEX 0x3:` and `SCAN dbstat VIRTUAL TABLE INDEX 0x2:`, hex index numbers).
- Not every module supports writes, transactions or `ALTER`.
- Create file-reading vtabs in `temp` so they are not persisted in the schema with machine-specific file names.

## Verify
`EXPLAIN QUERY PLAN` on a query against the vtab shows the module accepted the constraint (an index number other than 0, printed in hex in 3.54.1).
