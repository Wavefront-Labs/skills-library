---
id: computing-software.database-administration.schema-design.hierarchies-adjacency-closure-table-and-ltree
name: hierarchies-adjacency-closure-table-and-ltree
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, closure-table, adjacency-list, ltree, materialized-path, nested-sets, tree-queries, hierarchical-data]
level: practitioner
status: verified
description: "Store trees in SQL: adjacency list with recursive CTEs, closure tables for fast ancestor/descendant queries, and materialised paths with PostgreSQL ltree."
sources:
  - https://www.postgresql.org/docs/current/ltree.html
  - https://www.postgresql.org/docs/current/queries-with.html
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hierarchies: adjacency list, closure table, ltree

**Goal:** a tree model (categories, org charts, folders) whose common queries are fast and whose moves are manageable.

## Adjacency list (default)
```sql
CREATE TABLE categories (id bigint PRIMARY KEY, parent_id bigint REFERENCES categories(id), name text NOT NULL);
CREATE INDEX ON categories (parent_id);
```
Children: simple. Subtree / ancestors: `WITH RECURSIVE`. Moves: update one row. Fine for shallow trees or infrequent deep queries.

## Closure table
Store every ancestor-descendant pair with depth:
```sql
CREATE TABLE category_paths (
  ancestor bigint NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
  descendant bigint NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
  depth int NOT NULL,
  PRIMARY KEY (ancestor, descendant)
);
CREATE INDEX ON category_paths (descendant, ancestor);
-- insert node :n under parent :p (:n, :p are bind parameters; tested as a prepared statement)
INSERT INTO category_paths (ancestor, descendant, depth)
SELECT ancestor, :n, depth + 1 FROM category_paths WHERE descendant = :p
UNION ALL SELECT :n, :n, 0;
-- subtree of X
SELECT c.* FROM categories c JOIN category_paths p ON p.descendant = c.id WHERE p.ancestor = :x;
-- ancestors (breadcrumb)
SELECT c.* FROM category_paths p JOIN categories c ON c.id = p.ancestor WHERE p.descendant = :x ORDER BY p.depth DESC;
```
Moving a subtree: delete the links from outside ancestors to the subtree, then insert the cross product with the new parent's ancestors. Size is O(n x depth).

## Materialised path / ltree (PostgreSQL)
```sql
CREATE EXTENSION ltree;
CREATE TABLE categories2 (id bigint PRIMARY KEY, path ltree NOT NULL, name text);
CREATE INDEX ON categories2 USING gist (path);
SELECT * FROM categories2 WHERE path <@ 'root.electronics';         -- subtree
SELECT * FROM categories2 WHERE path @> 'root.electronics.tv.oled'; -- ancestors
SELECT * FROM categories2 WHERE path ~ 'root.*{1}';                  -- direct children of root
```
Labels are alphanumeric, underscore and hyphen, up to 1000 characters (PostgreSQL 18 manual); use IDs as labels so renames do not rewrite paths. Moving a subtree = update every descendant's prefix. `'new' || subpath(path, nlevel('old'))` fails with "invalid positions" on the subtree root itself (its path has exactly `nlevel('old')` labels), so special-case it:
```sql
UPDATE categories2 SET path = CASE WHEN path = 'root.electronics' THEN 'root.gadgets'
  ELSE 'root.gadgets' || subpath(path, nlevel('root.electronics')) END
WHERE path <@ 'root.electronics';
```

## Choosing
| Need | Pick |
|---|---|
| Mostly children, rare subtree queries | Adjacency list |
| Frequent subtree/ancestor queries, any DB, FK integrity | Closure table |
| PostgreSQL, fast subtree queries, simple storage | ltree |
| Read-mostly, ordered traversal | Nested sets (moves are expensive) |

## Verify
Subtree counts from the closure table or ltree match a recursive CTE over the adjacency list; after a test move, both agree again.
