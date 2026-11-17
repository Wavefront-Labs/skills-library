---
id: computing-software.database-administration.duckdb.duckdb-recursive-cte-using-key
name: duckdb-recursive-cte-using-key
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, recursive-cte, using-key, union-table, recurring, connected-components]
level: sme
status: docs-checked
description: "Use DuckDB WITH RECURSIVE ... USING KEY so later iterations overwrite earlier rows and can read the union table through recurring.<name>."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/with.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a recursive CTE behave like a dictionary instead of an append-only result.

A regular recursive CTE appends each iteration's rows to a union table. With `USING KEY (k)`, a row produced with key `k` replaces the existing row with the same key; if no such row exists it is appended. This keeps the union table small, which helps runtime and memory.

Inside such a CTE `T`, `T` denotes the rows added by the last iteration, and `recurring.T` denotes the union table built so far. Reading `recurring.T` during iteration is impossible in regular recursive CTEs.

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a) AS (
    SELECT a, b FROM (VALUES (1, 3), (2, 4)) t(a, b)
        UNION
    SELECT a + 1, b FROM tbl WHERE a < 3
)
SELECT * FROM tbl;
-- (1,3) (2,3) (3,3): key 2 payload 4 was overwritten by 3
```
Key columns are listed after `USING KEY`; the remaining columns are the payload that gets overwritten. The anchor can also be `VALUES (1, 3), (2, 4)`.

Connected components (lowest node id per component):

```sql
WITH RECURSIVE connected_components(id, comp) USING KEY (id) AS (
    SELECT n.id, n.id AS comp FROM nodes AS n
        UNION (
    SELECT DISTINCT ON (previous_iter.id) previous_iter.id, initial_iter.comp
    FROM recurring.connected_components AS previous_iter,
         connected_components AS initial_iter, edges AS e
    WHERE ((e.node1id, e.node2id) = (previous_iter.id, initial_iter.id)
        OR (e.node2id, e.node1id) = (previous_iter.id, initial_iter.id))
      AND initial_iter.comp < previous_iter.comp
    ORDER BY initial_iter.id ASC, previous_iter.comp ASC)
)
TABLE connected_components ORDER BY id;
```

Here `recurring.connected_components` holds the best component found so far per node, so a row is only replaced when a lower id is found.

The `nodes` and `edges` tables are the page's sample tables (`nodes(id)` with ids 1-8, `edges(node1id, node2id)`). See `duckdb-with-recursive` for the append-only form.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/query_syntax/with.md in full. Confirmed: USING KEY replace-or-append semantics like a dictionary, smaller union table helping runtime and memory, `T` versus `recurring.T`, the key/payload example with its result (1,3), (2,3), (3,3), the VALUES anchor, and the connected-components query and its result. Removed the invented Verify step. Added the sample-table note for the connected-components query.

Method: documentation only; no commands were run.
