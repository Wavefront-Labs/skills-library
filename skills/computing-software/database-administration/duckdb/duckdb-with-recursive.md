---
id: computing-software.database-administration.duckdb.duckdb-with-recursive
name: duckdb-with-recursive
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, recursive-cte, with-recursive, tree, graph, shortest-path, cycle-detection]
level: advanced
status: docs-checked
description: "Write DuckDB WITH RECURSIVE queries for sequences, tree paths and graph traversal with list-based cycle detection and unweighted shortest paths."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/with.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: iterate a query until it stops producing rows. A recursive CTE is an anchor query `UNION ALL` a recursive step that references the CTE name. You must ensure termination or the query loops forever. Mutually recursive CTEs are not supported.

Sequence (Fibonacci, depth-limited in the step's WHERE):
```sql
WITH RECURSIVE fib(depth, f, next) AS (
    SELECT 0, 0, 1
    UNION ALL
    SELECT depth + 1, next, f + next FROM fib WHERE depth + 1 < 10
)
SELECT depth, f FROM fib;
```

Tree path to the root (table `tag(id, name, subclassof)`):
```sql
WITH RECURSIVE tag_hierarchy(id, source, path) AS (
    SELECT id, name, [name] AS path FROM tag WHERE subclassof IS NULL
    UNION ALL
    SELECT tag.id, tag.name, list_prepend(tag.name, tag_hierarchy.path)
    FROM tag, tag_hierarchy WHERE tag.subclassof = tag_hierarchy.id
)
SELECT path FROM tag_hierarchy WHERE source = 'Oasis';   -- [Oasis, Rock, Music, Art]
```

Graph with cycles: keep the traversed path in a list and refuse revisits.
```sql
WITH RECURSIVE paths(startNode, endNode, path) AS (
    SELECT node1id, node2id, [node1id, node2id] FROM edge WHERE node1id = 1
    UNION ALL
    SELECT paths.startNode, node2id, array_append(path, node2id)
    FROM paths JOIN edge ON paths.endNode = node1id
    WHERE list_position(paths.path, node2id) IS NULL    -- all non-cyclic paths
)
SELECT * FROM paths ORDER BY length(path), path;
```
That enumerates all paths, not only shortest ones. For unweighted shortest paths, replace the filter with `WHERE NOT EXISTS (FROM paths previous_paths WHERE list_contains(previous_paths.path, node2id))` so a node already reached by an earlier (shorter) path is skipped.

Shortest paths between two nodes: add an `endReached` column, computed as `(node2id = 8)` in the anchor and `max(CASE WHEN node2id = 8 THEN 1 ELSE 0 END) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)` in the step, add `AND paths.endReached = 0`, then filter `WHERE endNode = 8`. The window function stops expansion once any new row reaches the end node.

For keyed overwrite semantics see `duckdb-recursive-cte-using-key`.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/query_syntax/with.md in full. Confirmed: termination warning, mutually recursive CTEs unsupported, the Fibonacci example (indexes 0 to 9 ending at 34), the tag tree example and its `[Oasis, Rock, Music, Art]` result, cycle prevention with a path list, the `NOT EXISTS ... list_contains` shortest-path variant, the `endReached` window-function technique for shortest paths between two nodes. Changes: removed the invented Verify step; the skill's anchor filter `WHERE node1id = 1` is an equivalent form of the page's `WHERE startNode = 1`.

Method: documentation only; no commands were run.
