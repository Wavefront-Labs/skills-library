---
id: computing-software.database-administration.cockroachdb.partial-indexes
name: partial-indexes
category: computing-software
field: database-administration
product: cockroachdb
tags: [partial-indexes, index-predicate, create-index-where, optimizer, write-overhead]
level: practitioner
status: docs-checked
description: "Use CockroachDB partial indexes (CREATE INDEX ... WHERE) to index only matching rows, reduce storage and write cost, and understand when the optimizer uses them."
sources:
  - https://www.cockroachlabs.com/docs/stable/partial-indexes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: index only the rows queries actually need.

Create with a `WHERE` predicate on `CREATE INDEX`:
```sql
CREATE INDEX ON t (a, b) WHERE c > 5;
```
Queries that can use it: `SELECT a, b FROM t WHERE c > 5;` and `SELECT * FROM t WHERE c = 10;` (the filter implies the predicate). A query without a filter that implies the predicate, such as `SELECT a, b FROM t;`, does not use it.

Benefits listed on the page:
- Smaller than full indexes, cheaper to create and store.
- Reads on matching rows scan only the partial index.
- Writes only touch the index when inserted rows satisfy the predicate, avoiding full-index write overhead.

Optimizer behaviour: the cost-based optimizer tries to prove the query filter implies the index predicate. It is not guaranteed to prove implications for arbitrarily complex expressions, so keep predicates simple and similar to how queries are written. If you force a partial index with an index hint and the filter does not imply the predicate, an error is returned.

Related: partial GIN indexes work the same way (`INVERTED INDEX ... WHERE ...`).

Verify: `EXPLAIN SELECT ...` names the partial index in the scan.

## Checked
2026-11-03. Confirmed on the partial indexes page: `CREATE INDEX ON t (a, b) WHERE c > 5;`, fewer rows to create and store, reads scan only partial index rows, writes only when inserted rows satisfy the predicate, the optimizer proving filter implies predicate (not guaranteed for complex expressions), index hints erroring when the predicate is not implied, partial GIN indexes. Removed: the fallback claim, silent regression gotcha and partial statistics remark.
Method: documentation only; no commands were run.
