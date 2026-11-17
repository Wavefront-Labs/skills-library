---
id: computing-software.database-administration.mysql.functional-key-parts-and-descending-indexes
name: functional-key-parts-and-descending-indexes
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, functional-key-parts, descending-index, functional-index, expression-index, mysql-indexing, generated-columns]
level: practitioner
status: verified
description: "Index expressions in MySQL 8 with functional key parts, use descending and mixed-order indexes for ORDER BY, and check that the optimizer actually uses them."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/create-index.html#create-index-functional-key-parts
  - https://dev.mysql.com/doc/refman/8.4/en/descending-indexes.html
  - https://dev.mysql.com/doc/refman/8.4/en/generated-column-index-optimizations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functional key parts and descending indexes

## Functional key parts (8.0.13+)
```sql
CREATE INDEX idx_email_lower ON users ((LOWER(email)));            -- note the double parentheses
CREATE INDEX idx_created_day ON orders ((DATE(created_at)));
CREATE INDEX idx_json_sku ON items ((CAST(attrs->>'$.sku' AS CHAR(32)) COLLATE utf8mb4_bin));
```
- Implemented as a hidden virtual generated column with an index.
- Queries must use the **same expression** to match: `WHERE LOWER(email) = 'a@b.c'` uses it; `WHERE email = ...` does not.
- JSON: the expression's type and collation must match the query's. A bare `((attrs->>'$.sku'))` is rejected (LONGTEXT cannot be indexed without a prefix, and functional key parts allow none per the CREATE INDEX docs), hence the CAST. On 9.7.4 with the index above, `WHERE CAST(attrs->>'$.sku' AS CHAR(32)) COLLATE utf8mb4_bin = 'S5'` and `WHERE attrs->>'$.sku' = 'S5'` both used `idx_json_sku`, but `WHERE CAST(attrs->>'$.sku' AS CHAR(32)) = 'S5'` (no COLLATE) did a full scan: always confirm with EXPLAIN. If the `mysql` client runs with a legacy client charset (cp850 on a Windows console) the `COLLATE utf8mb4_bin` clause fails with error 1253; start it with `--default-character-set=utf8mb4`.
- Multi-valued indexes for JSON arrays: `CREATE INDEX ON items ((CAST(attrs->'$.tags' AS CHAR(20) ARRAY)));` used by `MEMBER OF`, `JSON_CONTAINS`, `JSON_OVERLAPS` (all three showed `idx_tags` in EXPLAIN on 9.7.4).

Alternative: an explicit generated column + index, which also lets queries reference the column by name.

## Descending indexes (8.0+)
Before 8.0, `DESC` in an index definition was parsed and ignored. Now it is real:
```sql
CREATE INDEX idx_feed ON posts (user_id ASC, created_at DESC);
SELECT * FROM posts WHERE user_id = 7 ORDER BY created_at DESC LIMIT 20;   -- index range, no filesort
SELECT * FROM events ORDER BY priority DESC, created_at ASC LIMIT 50;     -- needs (priority DESC, created_at ASC)
```
Same-direction orderings can already be served by scanning an ASC index backward (EXPLAIN FORMAT=TREE shows `(reverse)` on the index lookup); DESC indexes matter for **mixed** directions. The manual says a reverse scan carries a performance penalty versus a forward scan (not measured here). On 9.7.4, `ORDER BY priority DESC, created_at ASC` forced onto an all-ASC index showed a `Sort:` node, and used `(priority DESC, created_at ASC)` with no sort.

## Verify
```sql
EXPLAIN FORMAT=TREE SELECT ...;
-- want: "Index lookup on users using idx_email_lower (lower(email) = ...)" / no "Sort:" node
SHOW INDEX FROM users;          -- Expression column shows the functional expression (lower(`email`)), Column_name is NULL
EXPLAIN SELECT ...;             -- 9.x default format is TREE; use EXPLAIN FORMAT=TRADITIONAL for the old table
```

## Gotchas
- Functional indexes cannot be primary keys (error 3756); expressions must be deterministic (`NOW()` and `RAND()` give error 3758 "disallowed function").
- Hidden generated columns count toward the table column limit (per the CREATE INDEX docs). They do not appear in `information_schema.COLUMNS` or `SHOW COLUMNS`; `SHOW EXTENDED COLUMNS FROM t` lists them as `!hidden!<index>!0!0` (VIRTUAL GENERATED). Tools that copy schemas must handle them (gh-ost/pt-osc behaviour not checked here).
- Collation mismatches between column and query literals defeat any index, functional or not.
