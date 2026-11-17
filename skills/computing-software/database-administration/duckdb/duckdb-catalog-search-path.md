---
id: computing-software.database-administration.duckdb.duckdb-catalog-search-path
name: duckdb-catalog-search-path
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, catalog, schema, search-path, use, qualified-names]
level: practitioner
status: docs-checked
description: "Resolve DuckDB object names across attached databases and schemas: catalog.schema.name, USE, ambiguity errors and the search_path setting."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/attach.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/create_table.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict which table a name refers to when several databases are attached.

A fully qualified name is `catalog.schema.name`, where the catalog is the attached database alias. The default database is the one the system launched with and the default schema is `main`. Unqualified names use the catalog search path, which by default contains the system catalog, the temporary catalog and the initially attached database with schema `main`.

```sql
ATTACH 'new_db.db';
CREATE SCHEMA new_db.my_schema;
CREATE TABLE new_db.my_schema.my_table (col INTEGER);
SELECT new_db.my_schema.my_table.col FROM new_db.my_schema.my_table;
```

`USE` changes the defaults:
```sql
USE new_db;            -- default becomes new_db.main
USE new_db.my_schema;  -- default becomes new_db.my_schema
```

Single qualifier: `new_db.tbl` is read as a catalog or a schema, whichever exists. With `ATTACH 'new_db.db'; CREATE SCHEMA my_schema;`, `CREATE TABLE new_db.tbl` creates `new_db.main.tbl` and `CREATE TABLE my_schema.tbl` creates `default_db.my_schema.tbl`. If a schema and a catalog share a name (`CREATE SCHEMA new_db;`), DuckDB raises `Binder Error: Ambiguous reference to catalog or schema "new_db" - use a fully qualified path like "memory.new_db"`.

Search path:
```sql
ATTACH ':memory:' AS db1;
ATTACH ':memory:' AS db2;
CREATE TABLE db1.tbl1 (i INTEGER);
CREATE TABLE db2.tbl2 (j INTEGER);
SET search_path = 'db1,db2';   -- comma-separated list
SELECT * FROM tbl1;
SELECT * FROM tbl2;
```

Temporary tables live in `temp.main` and take priority over same-named regular tables (see `duckdb-create-table`). See `duckdb-attach-detach` for attaching. The ATTACH page points to the keywords and identifiers page for database-name rules.

## Checked

2026-11-07. Read the ATTACH and DETACH page (Name Qualification section) and the CREATE TABLE page. Confirmed qualified names, default database and `main` schema, default search path contents, `USE` forms, single-qualifier resolution, the ambiguity Binder Error text, `search_path` as a comma-separated list, and that temporary tables are in `temp.main` and take priority in name resolution (CREATE TABLE page, added to sources). Removed the Verify step.

Method: documentation only; no commands were run.
