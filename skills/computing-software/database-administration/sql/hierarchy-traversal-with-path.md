---
id: computing-software.database-administration.sql.hierarchy-traversal-with-path
name: hierarchy-traversal-with-path
category: computing-software
field: database-administration
product: sql
tags: [sql, hierarchy-traversal-with-path]
level: practitioner
status: docs-checked
description: "Walk parent-child trees with a recursive CTE tracking depth and path."
sources: ["https://www.postgresql.org/docs/current/queries-with.html", "https://www.sqlite.org/lang_with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tree traversal with depth and path columns

- PostgreSQL: `WITH RECURSIVE t AS (SELECT id, parent_id, 0 AS depth, ARRAY[id] AS path FROM n WHERE parent_id IS NULL UNION ALL SELECT n.id, n.parent_id, t.depth+1, t.path || n.id FROM n JOIN t ON n.parent_id = t.id) SELECT * FROM t ORDER BY path;` The form is a non-recursive term, `UNION` or `UNION ALL`, then a recursive term that alone references the CTE.
- PostgreSQL: ordering by an array of visited ids gives depth-first order; ordering by a `depth` column gives breadth-first. Row order is otherwise not guaranteed (the page calls the natural breadth-first output an implementation detail), so always sort explicitly. PostgreSQL also has `SEARCH DEPTH FIRST BY id SET ordercol` and `SEARCH BREADTH FIRST BY ...` after the CTE, and `CYCLE` for loops.
- SQLite: the same `WITH RECURSIVE` shape works; the search order is controlled by an `ORDER BY` inside the recursive select. `ORDER BY level` (ascending) is breadth-first and `ORDER BY level DESC` is depth-first; with no `ORDER BY` the queue order is undefined (a FIFO in the current implementation).
- Cycles: if the links can loop the recursion never ends. `UNION` instead of `UNION ALL` discards duplicate rows but does not stop a loop when a depth or path column makes each row distinct; PostgreSQL tracks the path (`g.id = ANY(path)`) or uses `CYCLE`.
- Self-check: row count equals the number of reachable nodes; roots have depth 0.

## Checked

Date: 2026-11-07. Read PostgreSQL WITH Queries sections on recursive queries, search order (7.8.2.1) and cycle detection (7.8.2.2), and SQLite WITH clause recursive-CTE semantics and section 3.4 (depth-first versus breadth-first with ORDER BY). Confirmed the items above. Removed: the claim that SQLite uses a string path with `||` (not on the page) and "index parent_id or each level scans the table" (not on either page; indexing is plausible advice but unchecked here).
Method: documentation only; no commands were run.
