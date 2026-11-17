---
id: computing-software.database-administration.clickhouse.array-join-and-arrays
name: array-join-and-arrays
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, array-join, arrayjoin, arrays, unnest, group-by-all]
level: practitioner
status: docs-checked
description: "Expand array columns into rows in ClickHouse with ARRAY JOIN or arrayJoin and aggregate the result."
sources:
  - https://clickhouse.com/docs/reference/statements/select/array-join
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/starter_guides/working_with_arrays.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# array join and arrays
Arrays are a first-class column type. To turn each array element into its own row use `ARRAY JOIN` (the SQL clause form of the function `arrayJoin`):
```sql
SELECT del, count()
FROM ontime.ontime
ARRAY JOIN delay AS del
WHERE del > 0
GROUP BY ALL;
```
`ARRAY JOIN col AS alias` produces one output row per element, repeating the other columns. Rows whose array is empty vanish from the result, so use `LEFT ARRAY JOIN` when you must keep them (the empty-array value is the element type's default). Several comma-separated arrays are joined simultaneously (a direct sum, not a cartesian product) and by default must have the same size.

Gotcha: a row with several elements becomes several output rows, so `count()` after ARRAY JOIN counts elements, not parent rows.

## Checked
2026-11-03. Confirmed against the ClickHouse docs page "ARRAY JOIN clause": ARRAY JOIN versus LEFT ARRAY JOIN on empty arrays, default value for empty arrays, simultaneous join of multiple arrays of the same size. Removed: the memory advice and the Verify step.
Method: documentation only; no commands were run.
