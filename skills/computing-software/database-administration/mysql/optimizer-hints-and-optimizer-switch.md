---
id: computing-software.database-administration.mysql.optimizer-hints-and-optimizer-switch
name: optimizer-hints-and-optimizer-switch
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-optimization, optimizer-hints, optimizer-switch, index-hints, force-index, join-order, set-var-hint, query-rewrite]
level: advanced
status: verified
description: "Steer the MySQL optimizer when statistics fail: comment-style optimizer hints, index hints, SET_VAR, optimizer_switch flags, and the query rewrite plugin for code you cannot change."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/optimizer-hints.html
  - https://dev.mysql.com/doc/refman/8.4/en/switchable-optimizations.html
  - https://dev.mysql.com/doc/refman/8.4/en/index-hints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimizer hints and optimizer_switch

**Goal:** fix a specific bad plan surgically, after statistics and indexing have
been tried, and keep the fix discoverable.

## Optimizer hints (8.0, preferred)
Placed in a `/*+ ... */` comment right after SELECT/UPDATE/DELETE:
```sql
SELECT /*+ JOIN_ORDER(o, c) */ ... FROM customers c JOIN orders o ON ...;
SELECT /*+ INDEX(o idx_status_created) */ ... FROM orders o WHERE ...;      -- 8.0.20+
SELECT /*+ NO_INDEX_MERGE(t) BKA(t) */ ...;
SELECT /*+ MAX_EXECUTION_TIME(2000) */ ...;                                 -- ms, SELECT only
SELECT /*+ SET_VAR(optimizer_switch='derived_merge=off') SET_VAR(sort_buffer_size=16M) */ ...;
SELECT /*+ NO_RANGE_OPTIMIZATION(t) */ ...;
```
Unknown or invalid hints are ignored with a warning (`SHOW WARNINGS`), never an error: on 9.7.4 `/*+ FOO(o) */` gave warning 1064 "Optimizer hint syntax error", `INDEX(o idx_nonexist)` gave warning 3128 "Unresolved name ... for INDEX hint", and `MAX_EXECUTION_TIME` on an UPDATE gave warning 3125 (top-level standalone SELECT only). A hint is only a request: `INDEX(o idx_cid)` on a query that has no use for `idx_cid` still ran as a table scan. All hint lines above executed without error on 9.7.4.

## Index hints (older syntax, still common)
```sql
SELECT ... FROM orders FORCE INDEX (idx_status_created) WHERE ...;
SELECT ... FROM orders IGNORE INDEX (idx_created) ...;
```
FORCE INDEX makes a table scan look very expensive; it does not guarantee the
index is usable. A hint naming a dropped index **errors** (`ERROR 1176 Key 'idx' doesn't exist in table`, run on 9.7.4; unlike optimizer hints).

## optimizer_switch flags
```sql
SELECT @@optimizer_switch\G
SET SESSION optimizer_switch = 'index_merge_intersection=off';
```
Flags commonly toggled: `index_merge*`, `derived_merge`, `hash_join` (only had an effect in
8.0.18-8.0.19; the 8.4 manual says it has no effect, use `block_nested_loop`), `prefer_ordering_index` (stops choosing an ORDER BY index with LIMIT over a
selective filter index), `subquery_to_derived`. Change globally only after
regression testing; per statement via SET_VAR is safer. 9.7.4 `@@optimizer_switch` also lists `hypergraph_optimizer=off`, `derived_condition_pushdown=on` and `hash_set_operations=on`.

## Code you cannot change
Query Rewrite plugin: rewrite a normalised statement pattern to the hinted form. Install it first by running `share/install_rewriter.sql` from the server install (creates the `query_rewrite` schema and the plugin). Include `pattern_database`, otherwise unqualified table names fail to load.
```sql
INSERT INTO query_rewrite.rewrite_rules (pattern_database, pattern, replacement) VALUES
('appdb', 'SELECT * FROM orders WHERE status = ?', 'SELECT /*+ INDEX(orders idx_status) */ * FROM orders WHERE status = ?');
CALL query_rewrite.flush_rewrite_rules();
SELECT id, enabled, message FROM query_rewrite.rewrite_rules;   -- message must be NULL
```
Without `pattern_database` the flush raised `ERROR 1644 Loading of some rule(s) failed` and `message` read `Parse error in pattern: >>No database selected<<` (9.7.4). After a good load, running the statement (not `EXPLAIN` of it) produced note 1105 "... rewritten to ... by a query rewrite plugin" and `Rewriter_number_rewritten_queries` incremented; `EXPLAIN` of the same statement was not rewritten.

## Gotchas
- Hints freeze today's best plan; data growth can make it wrong. Comment why and
  revisit.
- Some ORMs, proxies and query builders strip comments; confirm the hint
  reached the server with `EXPLAIN` + `SHOW WARNINGS` (the rewritten statement
  shows the hints that were applied).
- MariaDB supports index hints and `optimizer_switch`; the `/*+ ... */` hint comments above are MySQL 8 syntax, so check MariaDB's docs before relying on them there (not run here).

## Verify
`EXPLAIN` shows the intended index/join order, and `SHOW WARNINGS` after EXPLAIN
has no "hint ignored" messages.
