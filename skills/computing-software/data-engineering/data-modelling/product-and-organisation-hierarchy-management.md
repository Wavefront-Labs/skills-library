---
id: computing-software.data-engineering.data-modelling.product-and-organisation-hierarchy-management
name: product-and-organisation-hierarchy-management
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, hierarchy-management, parent-child-hierarchy, ragged-hierarchy, bridge-table, closure-table, slowly-changing-hierarchy]
level: practitioner
status: draft
description: "Model and manage product and organisation hierarchies: parent-child vs levelled, ragged and unbalanced trees, closure and bridge tables, versioning changes, and alternate rollups."
sources:
  - https://docs.snowflake.com/en/sql-reference/constructs/connect-by
  - https://www.postgresql.org/docs/current/queries-with.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hierarchy management (product / org hierarchies)

## Shapes
| Shape | Example | Model |
|---|---|---|
| Fixed levels, balanced | Category > Subcategory > Product | flattened columns in the dimension (`category`, `subcategory`) |
| Ragged (levels skipped) | some products have no subcategory | flattened with backfilled levels or bridge table |
| Variable depth (unbalanced) | org chart, chart of accounts, BOM | parent-child source + closure/bridge table for BI |
| Multiple alternate hierarchies | sales region vs legal entity rollup | separate hierarchy tables keyed by `hierarchy_id` |

## Source of truth: parent-child with effective dating
```sql
CREATE TABLE org_unit_hierarchy (
  hierarchy_id   TEXT NOT NULL,         -- 'MANAGEMENT', 'LEGAL'
  node_id        TEXT NOT NULL,
  parent_node_id TEXT,                  -- NULL for root
  valid_from     DATE NOT NULL,
  valid_to       DATE NOT NULL DEFAULT '9999-12-31',
  PRIMARY KEY (hierarchy_id, node_id, valid_from)
);
```
Rules enforced in MDM or tests: exactly one root per hierarchy, no cycles, every parent exists at the same validity date, no node with two parents at once (unless the hierarchy allows weighted multi-parent rollups).

## Closure table for queries
```sql
WITH RECURSIVE tree AS (
  SELECT node_id AS ancestor_id, node_id AS descendant_id, 0 AS depth
  FROM org_unit_hierarchy WHERE hierarchy_id = 'MANAGEMENT' AND CURRENT_DATE BETWEEN valid_from AND valid_to
  UNION ALL
  SELECT t.ancestor_id, h.node_id, t.depth + 1
  FROM tree t JOIN org_unit_hierarchy h ON h.parent_node_id = t.descendant_id
   AND h.hierarchy_id = 'MANAGEMENT' AND CURRENT_DATE BETWEEN h.valid_from AND h.valid_to
)
SELECT * FROM tree;
```
Join facts on `descendant_id` and filter `ancestor_id = 'EMEA'` to roll up everything under EMEA at any depth. Snowflake/Oracle also offer `CONNECT BY`; dbt packages can materialise closure tables.

## Flattening for BI tools
Many BI tools want fixed level columns. Flatten to N levels and backfill short branches (repeat the leaf name or "No subcategory") so drill-down doesn't show blanks. Keep `path` (`/Global/EMEA/UK`) and `depth` columns for search and sorting.

## Changes over time
- Reorganisations: close the old edge (`valid_to`) and open a new one; never update in place, or historical reports silently restate.
- Decide reporting semantics per use case: **as-was** (facts rolled up by the hierarchy valid at transaction date) vs **as-is** (current hierarchy restates history). Offer both by joining on date or current version.
- Type 2 on the dimension for node attributes (name, manager) separate from structure changes.

## Governance
- Hierarchy changes go through stewardship workflow (request, approval, effective date), often in the MDM tool.
- Publish hierarchies as reference datasets with version IDs consumed by finance, sales ops and the warehouse.

## Verify
- [ ] Tests: single root, no cycles, no orphan parents, no overlapping validity for a node.
- [ ] Rollup totals at the root equal the sum of leaf facts for both as-was and as-is views.
