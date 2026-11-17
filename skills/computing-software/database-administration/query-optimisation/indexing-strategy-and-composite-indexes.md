---
id: computing-software.database-administration.query-optimisation.indexing-strategy-and-composite-indexes
name: indexing-strategy-and-composite-indexes
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, indexing, composite-index, covering-index, index-column-order, leftmost-prefix, sargability, over-indexing, write-amplification, b-tree, index-only-scan]
level: advanced
status: draft
description: "Design composite and covering indexes in the right column order for real WHERE/ORDER BY patterns, and recognize when a predicate silently can't use an index at all."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexing strategy: composite index column order, covering indexes, and sargability

**Goal:** design indexes that match how queries actually filter and sort, not one
index per column, and recognize the specific predicate shapes that can't use an
index no matter how many you add.

## 1. Column order in a composite index is not a style choice
A B-tree composite index `(a, b, c)` is only useful as a **leftmost prefix**: a
query filtering on `a` alone, `a AND b`, or `a AND b AND c` can use it; a query
filtering on `b` alone or `c` alone generally cannot (it would need a full scan of
the index, usually not chosen by the planner over a table scan). The standard
ordering heuristic:
1. **Equality columns first** (`WHERE a = ? AND b = ?`) — these narrow the search
   the most per column.
2. **Then the single sort/range column** that matches `ORDER BY` or a range
   predicate (`WHERE c > ?`) — a range or sort column must come after all equality
   columns, and only one range/sort column gets the benefit; once the index hits a
   range comparison, later columns in the index can't be used to narrow further
   within that range in the same way.
3. High-cardinality columns generally make better leading columns than
   low-cardinality ones (an index starting with a boolean filters almost nothing).

## 2. Covering indexes: skip the table entirely
Adding columns the query only `SELECT`s (not filters on) to the end of the index
lets the engine answer the query from the index alone — an "index-only scan"
(Postgres), "covering index" (SQL Server `INCLUDE`), or similar, avoiding a trip to
the heap/clustered table for every matching row. This is the single biggest
win available for a hot, narrow read query, and is routinely missed because people
think of indexes purely in terms of `WHERE` clauses. Check with `EXPLAIN` that the
plan actually says "Index Only Scan" / shows no key lookup — adding INCLUDE columns
without verifying the engine used them is a common silent miss (e.g. a visibility
map not being all-visible yet in Postgres MVCC can still force heap fetches).

## 3. Sargability: predicates that can't use an index as written
"Search ARGument ABLE" — some predicate shapes defeat index use regardless of
what's indexed:
- `WHERE function(column) = value` (e.g. `WHERE LOWER(email) = 'x'`) — the index
  is on `column`, not `function(column)`; needs a matching **functional/expression
  index** on `LOWER(email)` specifically, or rewriting to avoid wrapping the
  column.
- `WHERE column LIKE '%term'` (leading wildcard) — can't use a standard B-tree
  prefix scan; needs a trigram/full-text index if this pattern is common.
- `WHERE column + 1 = value` or any arithmetic/cast on the indexed column —
  same problem as the function case; keep the indexed column bare on one side of
  the comparison, computation on the literal side instead.
- Implicit type coercion (comparing a text column to a number, or an untyped
  parameter in some drivers) can silently force a cast on the column side too —
  check the actual plan, not just the SQL text, when an index "should" apply but
  doesn't.

## 4. Over-indexing has a real cost
Every index is maintained on every write — a table with 15 indexes pays 15
updates (plus WAL/undo/redo volume) per row change, often dwarfing the cost of the
base table write itself, and each index consumes buffer-pool/cache space competing
with the ones that matter. Periodically find unused indexes (engine-specific usage
stats: `pg_stat_user_indexes.idx_scan`, SQL Server's missing/unused index DMVs,
MySQL's `sys.schema_unused_indexes`) and drop them — "it might be used someday" is
not a reason to keep paying the write cost indefinitely.

## 5. Multi-column vs. multiple single-column indexes
Most engines can combine two single-column indexes via a bitmap/index
intersection for an `AND` query, but a purpose-built composite index is almost
always more efficient than relying on intersection — don't assume intersection
makes individual indexes an adequate substitute for a composite one on a hot query
path; verify with `EXPLAIN` which strategy the planner actually picked.

## Verify
- [ ] Composite index column order was chosen from actual query predicates (equality, then one range/sort column), not column position in the table.
- [ ] A hot, narrow read query was checked for whether a covering index would produce an index-only scan.
- [ ] Any `WHERE` clause wrapping the indexed column in a function/cast was checked against the plan, not assumed to use the index.
- [ ] Index usage stats were reviewed in the last quarter and genuinely unused indexes were dropped.
- [ ] `EXPLAIN` output (not intuition) confirmed which index, if any, a representative hot query actually uses.
