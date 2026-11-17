---
id: computing-software.database-administration.duckdb.duckdb-pragma-metadata-introspection
name: duckdb-pragma-metadata-introspection
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, pragma, metadata, table-info, database-size, storage-info]
level: intro
status: docs-checked
description: "Inspect a DuckDB instance with PRAGMAs: database_list, show_tables, table_info, database_size, storage_info, version, platform, plus errors_as_json."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/configuration/pragmas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find out what a database contains, how big it is, and how it is stored, using PRAGMAs and their `pragma_*` table-function twins.

Schema listing:

```sql
PRAGMA database_list;
PRAGMA show_databases;          -- same as SHOW DATABASES
PRAGMA show_tables;
PRAGMA show_tables_expanded;    -- like DESCRIBE, with extra detail
PRAGMA functions;
PRAGMA collations;
```
Where thousands of databases are attached, "did you mean..." catalog errors get slow; limit how many schemas DuckDB looks through with `SET catalog_error_max_schemas = 10;`.

Columns of a table:

```sql
PRAGMA table_info('table_name');   -- or CALL pragma_table_info('table_name');
-- cid, name, type, notnull, dflt_value, pk
```

Size and memory per database:

```sql
PRAGMA database_size;   -- or CALL pragma_database_size();
-- database_name, database_size, block_size, total_blocks, used_blocks, free_blocks,
-- wal_size, memory_usage, memory_limit
```
`database_size` is the total block count times the block size; `memory_usage` is memory used by the buffer manager.

Physical layout:

```sql
PRAGMA storage_info('table_name');   -- or CALL pragma_storage_info('table_name');
-- row_group_id, column_name, column_id, column_path, segment_id, segment_type,
-- start, count, compression, stats, has_updates, persistent, block_id, block_offset
```
`compression` is the compression type used for the column; `persistent` is false for a temporary table; `block_id` and `block_offset` are empty unless persistent.

Environment: `PRAGMA version;` (or `CALL pragma_version()`), `PRAGMA platform;` (for example `osx_arm64`, matches extension platform names), `PRAGMA user_agent;`, `PRAGMA metadata_info;` (block_id, total_blocks, free_blocks, free_list of the metadata store).

Machine-readable errors: `SET errors_as_json = true;` makes errors come back as JSON with fields such as `exception_type`, `exception_message`, `name`, `candidates`, `position`, `type`, `error_subtype`.

PRAGMAs that assign a value can be written as `SET`, and read back with `SELECT current_setting(name)` (see duckdb-configuration-settings). Related: duckdb-profiling-settings, duckdb-storage-checkpoint-tuning.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page configuration/pragmas.md in full. Confirmed: database_list, show_tables, show_tables_expanded, functions, collations, show_databases, `catalog_error_max_schemas`, table_info, database_size and storage_info column lists with their `CALL pragma_*` forms, version, platform (`osx_arm64`), user_agent, metadata_info columns, `errors_as_json` fields, SET/PRAGMA equivalence and `current_setting`. Removed: the "(default 100)" for `catalog_error_max_schemas` (not on the page), the unsupported advice about free blocks and WAL size, and the invented Verify step. Reworded `compression` to the page's description.

Method: documentation only; no commands were run.
