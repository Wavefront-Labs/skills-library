---
id: computing-software.database-administration.sqlite.inspecting-schema-in-sqlite
name: inspecting-schema-in-sqlite
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-schema-inspection, sqlite-schema, pragma-table-info, sqlite3-shell, sqlite-cli]
level: practitioner
status: verified
description: "Inspect a SQLite database schema with .schema, .tables, .indexes, sqlite_schema queries and table-valued pragmas (table_xinfo, index_list, foreign_key_list)."
sources:
  - https://sqlite.org/cli.html#querying_the_database_schema
  - https://sqlite.org/schematab.html
  - https://sqlite.org/pragma.html#pragfunc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Querying the schema

## Shell dot-commands
```text
.tables                    -- table and view names (.tables 'ord%' to filter)
.schema orders             -- CREATE statements for orders and its indexes/triggers
.schema --indent           -- pretty-printed
.indexes orders            -- index names on a table
.fullschema                -- schema plus sqlite_stat tables (useful for planner bug reports)
.dbinfo                    -- page size, encoding, schema cookie, user_version
```

## sqlite_schema (formerly sqlite_master)
```sql
SELECT type, name, tbl_name, sql FROM sqlite_schema WHERE type IN ('table','index','view','trigger') ORDER BY type, name;
```
`sqlite_temp_schema` for temp objects. Auto-indexes (`sqlite_autoindex_*`) back UNIQUE/PRIMARY KEY constraints and have `sql IS NULL`.

## Table-valued pragma functions (3.16+): queryable and joinable
```sql
SELECT * FROM pragma_table_xinfo('orders');         -- cid, name, type, notnull, dflt_value, pk, hidden (generated cols)
SELECT * FROM pragma_index_list('orders');           -- seq, name, unique, origin (c=create index, u=unique, pk), partial
SELECT * FROM pragma_index_xinfo('idx_orders_cust'); -- columns incl. key/aux and sort order
SELECT * FROM pragma_foreign_key_list('order_items');
```
All columns of all tables in one query:
```sql
SELECT m.name AS tbl, p.name AS col, p.type, p."notnull", p.pk
FROM sqlite_schema m JOIN pragma_table_info(m.name) p
WHERE m.type = 'table' AND m.name NOT LIKE 'sqlite_%' ORDER BY 1, p.cid;
```
Find tables without indexes on their foreign key columns:
```sql
SELECT m.name, f."from" FROM sqlite_schema m JOIN pragma_foreign_key_list(m.name) f
WHERE m.type='table' AND NOT EXISTS (
  SELECT 1 FROM pragma_index_list(m.name) il JOIN pragma_index_info(il.name) ii
  WHERE ii.name = f."from" AND ii.seqno = 0);
```

## Gotchas
- Declared types are free text (affinity rules apply); `pragma_table_info.type` shows the declared text (`varchar(10)`, `MyType` came back as written; plain `int`, `integer`, `text` came back uppercased as `INT`, `INTEGER`, `TEXT`), and it is not enforced unless the table is STRICT.
- `pragma_table_xinfo.hidden` was 2 for a virtual generated column in a test (0 for ordinary columns); `.dbinfo` printed `user version` and `schema cookie`.
- `ALTER TABLE` edits the stored SQL text; old schemas may have odd formatting.

## Verify
Compare `.schema` output to your migration files in CI to detect drift (dump schema, normalise, diff).
