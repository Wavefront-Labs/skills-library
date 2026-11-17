---
id: computing-software.database-administration.schema-design.self-referencing-relationships
name: self-referencing-relationships
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, self-referencing, recursive-relationship, adjacency-list, hierarchies, foreign-keys]
level: practitioner
status: verified
description: "Model self-referencing relationships (employee manager, category parent, bill of materials) with self-FKs, cycle prevention, deletion rules and recursive queries."
sources:
  - https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
  - https://learn.microsoft.com/en-us/sql/relational-databases/hierarchical-data-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-referencing relationships

## One-to-many on the same table
```sql
CREATE TABLE employees (
  id bigint PRIMARY KEY,
  name text NOT NULL,
  manager_id bigint REFERENCES employees(id) ON DELETE SET NULL,
  CHECK (manager_id <> id)                        -- no self-management
);
CREATE INDEX ON employees (manager_id);            -- find direct reports; needed for FK deletes
```
Root rows have `manager_id IS NULL`. Insert order: parents first, or make the FK `DEFERRABLE INITIALLY DEFERRED` for bulk loads.

## Many-to-many on the same table
Bill of materials, social follows, related products:
```sql
CREATE TABLE part_components (
  parent_part_id bigint REFERENCES parts(id),
  child_part_id  bigint REFERENCES parts(id),
  qty numeric NOT NULL CHECK (qty > 0),
  PRIMARY KEY (parent_part_id, child_part_id),
  CHECK (parent_part_id <> child_part_id));
```
Symmetric relationships (friendship) either store both directions or one canonical direction (`CHECK (a < b)`).

## Querying the tree
```sql
WITH RECURSIVE chain AS (
  SELECT id, manager_id, name, 1 AS depth, ARRAY[id] AS path FROM employees WHERE id = 42
  UNION ALL
  SELECT e.id, e.manager_id, e.name, c.depth + 1, c.path || e.id
  FROM employees e JOIN chain c ON e.manager_id = c.id
  WHERE NOT e.id = ANY(c.path)                     -- cycle guard
)
SELECT * FROM chain;
```
PostgreSQL 14+ adds the SQL-standard `CYCLE id SET is_cycle USING path` clause (14 release notes; run on 18, it flagged the repeated node). Other engines have their own guards (check docs).

## Preventing cycles
A CHECK cannot see other rows (checked: `UPDATE employees SET manager_id = 3 WHERE id = 1` creating a 1-2-3-1 cycle succeeded, while `manager_id = id` was rejected by the CHECK). Options: trigger that walks ancestors before insert/update of `manager_id`; or closure table / ltree path models where cycles are detectable by path prefix. Without prevention, a cycle makes recursive queries loop until guards stop them.

## Deletion rules
- `ON DELETE SET NULL`: orphans become roots (fine for managers).
- `ON DELETE CASCADE`: deletes whole subtrees (dangerous for categories with products).
- `RESTRICT`: force reassignment first (often correct: "reassign reports before removing a manager").

## When adjacency list is not enough
Deep, read-heavy hierarchies with subtree queries: closure tables, materialised paths (ltree, `hierarchyid`) or nested sets.

## Verify
Test inserting a cycle (A→B→A) is rejected by your chosen mechanism, and the recursive query returns the expected subtree for a known node.
