---
id: computing-software.data-engineering.databricks.unity-catalog-information-schema-queries
name: unity-catalog-information-schema-queries
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, uc-information-schema, unity-catalog, metadata-queries, governance]
level: practitioner
status: docs-checked
description: "Answer governance questions with Unity Catalog information_schema: find tables, owners, columns, tags, privileges and undocumented objects across catalogs."
sources:
  - https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-information-schema
  - https://docs.databricks.com/aws/en/sql/language-manual/information-schema/tables
  - https://docs.databricks.com/aws/en/sql/language-manual/information-schema/column_tags
  - https://docs.databricks.com/aws/en/sql/language-manual/information-schema/table_privileges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity Catalog information schema queries

**Goal:** inventory and audit metadata with SQL instead of clicking through Catalog Explorer.

## Where
- `system.information_schema.*`: all catalogs in the metastore that you can see (not `hive_metastore` objects).
- `<catalog>.information_schema.*`: one catalog, created automatically with each catalog.
Views include `catalogs`, `schemata`, `tables`, `columns`, `views`, `volumes`, `table_privileges`, `schema_privileges`, `catalog_privileges`, `column_tags`, `table_tags`, `schema_tags`, `routines`, `table_constraints`, `key_column_usage`. No explicit `SELECT` grant is needed.

## Useful queries
```sql
-- tables without comments, by owner
SELECT table_catalog, table_schema, table_name, table_owner
FROM system.information_schema.tables
WHERE comment IS NULL AND table_schema <> 'information_schema';

-- columns that look like PII and have no tag
SELECT c.table_catalog, c.table_schema, c.table_name, c.column_name
FROM system.information_schema.columns c
LEFT JOIN system.information_schema.column_tags t
  ON t.catalog_name = c.table_catalog AND t.schema_name = c.table_schema
 AND t.table_name = c.table_name AND t.column_name = c.column_name
WHERE c.column_name RLIKE '(?i)email|phone|ssn|birth' AND t.tag_name IS NULL;

-- who has access to a table
SELECT grantee, privilege_type FROM system.information_schema.table_privileges
WHERE table_catalog = 'main' AND table_schema = 'sales' AND table_name = 'orders';

-- stale tables
SELECT table_catalog, table_schema, table_name, last_altered
FROM system.information_schema.tables WHERE last_altered < current_date() - INTERVAL 180 DAYS;
```

## Gotchas
- Results are automatically filtered to the objects your Unity Catalog privileges let you see, so audit as a principal with sufficient access.
- `table_privileges` has an `inherited_from` column for privileges inherited from an ancestor. Users with `MANAGE` currently see only their own grants there; use SHOW GRANTS or Catalog Explorer to see all grants.
- Apply selective filters (for example `table_catalog` and `table_schema`) to avoid timeouts; `LIMIT` is not pushed down. Identifiers other than column and tag names are stored lowercase, so compare with lowercase values instead of wrapping columns in `LOWER()`.
- Some catalog metadata changes may need `REPAIR TABLE` before they show in the information schema.
- Access events are in the audit log system table, not in the information schema.

## Verify
Spot-check one result in Catalog Explorer (owner, comment, grants match).

## Checked

2026-11-09. Confirmed on the Databricks information schema overview and the TABLES, COLUMN_TAGS and TABLE_PRIVILEGES reference pages: system and per-catalog information schemas, privilege-aware filtering without a SELECT grant, the list of views, column names used in the queries (table_owner, comment, last_altered, catalog_name, schema_name, tag_name, grantee, privilege_type, inherited_from), MANAGE limitation, filtering and lowercase identifier notes, REPAIR TABLE note. COLUMNS columns table_catalog, table_schema and column_name also confirmed.

Method: documentation only; no commands were run.

