---
id: computing-software.database-administration.duckdb.duckdb-unnest
name: duckdb-unnest
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, unnest, list, struct, flatten, recursive, generate-subscripts]
level: practitioner
status: docs-checked
description: "Expand DuckDB lists and structs into rows or columns with unnest, including recursive and max_depth options, side-by-side padding and tracking element positions."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/unnest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: flatten nested data. `unnest` is a special function usable only in the `SELECT` clause; it unnests one level by default.

Lists give one row per element; other scalar expressions in the SELECT repeat on every row. Multiple unnested lists run side by side and the shorter is padded with NULL. Empty and NULL lists give zero rows.

```sql
SELECT unnest([1, 2, 3]);                        -- 3 rows
SELECT unnest([1, 2, 3]), 10;                    -- (1,10),(2,10),(3,10)
SELECT unnest([1, 2, 3]), unnest([10, 11]);      -- (1,10),(2,11),(3,NULL)
SELECT unnest(l) + 10 FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
SELECT unnest([]);   SELECT unnest(NULL);        -- no rows
```

Structs give one column per field: `SELECT unnest({'a': 42, 'b': 84});` returns columns a, b.

Recursive: `recursive := true` fully unnests lists first, then structs; lists inside structs are not unnested.

```sql
SELECT unnest([[1, 2, 3], [4, 5]], recursive := true);                        -- 5 rows
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true); -- 2 rows, cols a,b
```

`max_depth := n` limits depth and implies recursive. For `[[[1,2],[3,4]],[[5,6],[7,8,9],[]],[[10,11]]]`, depth 2 yields the lists `[1,2] [3,4] [5,6] [7,8,9] [] [10,11]`; depth 3 yields the integers 1 to 11.

Element positions: combine with `generate_subscripts`:

```sql
SELECT unnest(l) AS x, generate_subscripts(l, 1) AS index
FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);   -- index restarts at 1 per list
```

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/query_syntax/unnest.md in full. Confirmed: SELECT-clause-only special function, one level by default, row per list entry, repeated scalars, side-by-side padding with NULL, empty and NULL lists giving zero rows, struct columns, `recursive := true` order and the lists-within-structs note, `max_depth` implying recursion with the depth 2 and 3 results, `generate_subscripts` example and its restarting index. Removed: the invented Verify step.

Method: documentation only; no commands were run.
