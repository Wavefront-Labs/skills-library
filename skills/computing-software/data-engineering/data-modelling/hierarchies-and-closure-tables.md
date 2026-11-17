---
id: computing-software.data-engineering.data-modelling.hierarchies-and-closure-tables
name: hierarchies-and-closure-tables
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, closure-table, hierarchical-data, adjacency-list, recursive-cte, org-hierarchy, path-enumeration, flattened-hierarchy, ragged-hierarchy]
level: advanced
status: gated
description: "Model hierarchies (org charts, category trees, BOMs) as adjacency lists, closure tables, path strings or flattened levels, with recursive CTEs and roll-up queries."
sources:
  - https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Hierarchies and closure tables

**Goal:** answer "everything under node X" and "roll up to every ancestor" efficiently for trees of any depth.

## Representations
| Model | Storage | Subtree query | Updates | Best for |
|---|---|---|---|---|
| Adjacency list (`parent_id`) | 1 row/node | recursive CTE | trivial | OLTP source of truth |
| Closure table (ancestor, descendant, depth) | O(n x depth) | simple join | rebuild affected paths | analytics roll-ups, variable depth |
| Path string (`/1/4/9/`) | 1 row/node | `like '/1/4/%'` | rewrite subtree paths | simple trees, sorting |
| Flattened levels (`level1..level6`) | 1 row/node | filter on column | rebuild | BI tools with fixed-depth drill-down |

## Recursive CTE over an adjacency list
```sql
with recursive tree as (
  select id, parent_id, name, 0 as depth, cast(id as varchar) as path
  from org_unit where parent_id is null
  union all
  select c.id, c.parent_id, c.name, t.depth + 1, t.path || '/' || c.id
  from org_unit c join tree t on c.parent_id = t.id
)
select * from tree;
```
Guard against cycles in dirty data: stop at a max depth (`where t.depth < 50`). Do not test `position(c.id in t.path)`: it is a substring match, so id 1 is found inside the path `10/2` (tested); compare delimited tokens, e.g. `contains('/' || t.path || '/', '/' || c.id || '/')`. Snowflake also supports `CONNECT BY` (gated: unconfirmed, source is paywalled or blocked). The recursive CTE, closure build, roll-up and split_part flattening were run on DuckDB 1.5 with a 5-node tree: closure rows 12 = sum(depth+1), root roll-up 150 = grand total.

## Build a closure table
```sql
create table org_closure as
with recursive c as (
  select id as ancestor_id, id as descendant_id, 0 as depth from org_unit
  union all
  select c.ancestor_id, o.id, c.depth + 1
  from c join org_unit o on o.parent_id = c.descendant_id
)
select * from c;
```
Includes self rows (depth 0) so roll-ups include a node's own facts.

## Roll-up with a closure table (bridge)
```sql
-- total sales for each org unit including all descendants
select a.name as org_unit, sum(f.amount) as total_sales
from org_closure cl
join org_unit a on a.id = cl.ancestor_id
join fct_sales f on f.org_unit_id = cl.descendant_id
group by a.name;
```
This is Kimball's hierarchy bridge table. Each fact row is counted once per ancestor, which is correct for roll-ups; filter on one ancestor to avoid double counting in totals.

## Flattening for BI
```sql
select id,
  split_part(path, '/', 1) as level1_id, split_part(path, '/', 2) as level2_id, ...
```
Ragged trees: fill missing lower levels with the last known ancestor (or "n/a") so drill-downs do not show blanks.

## Slowly changing hierarchies
Reorgs: snapshot the closure table with `valid_from/valid_to`, or rebuild daily and keep date-stamped copies, so historical reports can use the hierarchy as it was.

## Verify
- [ ] Closure row count = sum over nodes of (depth + 1); no cycles detected.
- [ ] Root roll-up total equals the grand total of facts.
