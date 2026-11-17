---
id: computing-software.database-administration.sqlite.expert-index-suggestions
name: expert-index-suggestions
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3-cli, sqlite-expert, dot-expert, index-advisor, explain-query-plan, query-tuning]
level: practitioner
status: verified
description: "Use the sqlite3 shell's .expert mode to get recommended indexes for a slow query, then validate the suggestion with EXPLAIN QUERY PLAN before creating it."
sources:
  - https://sqlite.org/cli.html#index_recommendations_sqlite_expert_
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .expert index recommendations

**Goal:** a quick, evidence-based index suggestion for a SQLite query without
guessing column order.

## Use
```
sqlite3 app.db
sqlite> .expert
sqlite> SELECT id, total FROM orders WHERE customer_id = 42 AND status = 'open' ORDER BY created_at DESC;
CREATE INDEX orders_idx_ddd6daa5 ON orders(customer_id, status, created_at DESC);

SEARCH orders USING INDEX orders_idx_ddd6daa5 (customer_id=? AND status=?)
```
(Output from the 3.54.1 shell on a 2000-row test table; the index name is a hash and the
equality columns come out in the order the planner picked, here `customer_id, status`.)
`.expert` applies to the **next** statement only; it does not execute it. It
proposes indexes, then shows the plan the query would get with them.
Options (cli.html documents the double-dash forms; the single-dash `-verbose` and `-sample 25`
also ran in 3.54.1): `.expert --verbose` (adds a `-- Candidates` list and each candidate's plan),
`--sample PERCENT` (gather statistics from PERCENT percent of the rows; default 0 uses the
schema and query alone, as the planner does without ANALYZE).

## Then decide
1. Check whether an existing index nearly fits (extend it rather than adding another).
2. Reorder columns if other queries share a prefix (equality columns first, then the ORDER BY column).
3. Create it with a meaningful name and run `ANALYZE` (or `PRAGMA optimize`).
4. Re-check with `EXPLAIN QUERY PLAN` that the plan changed as predicted.

## Gotchas
- Suggestions optimise one query; every index slows inserts and grows the file.
- `.expert` is built from the SQLite expert extension code and ran in the sqlite.org 3.54.1
  shell; other shells (distro builds, the Python module has no shell) may omit it. The .expert
  analysis opens additional connections, which matters if the database relies on
  extensions or custom functions (cli.html).
- Programmatic equivalent: the `sqlite3expert` C API in `ext/expert`.

## Verify
After creating the index, `.timer on` shows the query faster and
`EXPLAIN QUERY PLAN` uses the new index without `TEMP B-TREE`.
