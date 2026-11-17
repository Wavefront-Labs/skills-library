---
id: computing-software.database-administration.duckdb.duckdb-logging
name: duckdb-logging
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, logging, enable-logging, duckdb-logs, http, querylog, debugging]
level: practitioner
status: docs-checked
description: "Use DuckDB's logging: enable_logging, levels, log types (QueryLog, HTTP, FileSystem), memory/stdout/file storage, buffer size for crash debugging."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/logging/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: capture query, HTTP or file-system events for debugging and auditing.

Warning: logs can contain secrets and credentials. Control where they are stored and review before sharing.

Basics:

```sql
CALL enable_logging();                 -- default level INFO, in-memory storage
SELECT * FROM duckdb_logs;             -- view over the active storage
CALL truncate_duckdb_logs();           -- clear
CALL disable_logging();
```
Levels: `ERROR`, `WARN`, `INFO` (default), `DEBUG`, `TRACE`; set with `CALL enable_logging(level = 'debug');`.

Log types narrow what is written. `CALL enable_logging('HTTP');` sets the right level and adds the type to `enabled_log_types`; several: `CALL enable_logging(['HTTP', 'QueryLog']);`. Known types (non-exhaustive): `QueryLog` (executed queries, unstructured), `FileSystem` (structured), `HTTP` (internal HTTP client traffic, structured). Parse structured messages with `duckdb_logs_parsed('HTTP')`, e.g. `SELECT request.headers FROM duckdb_logs_parsed('HTTP');`; see the schema with `DESCRIBE FROM duckdb_logs_parsed('HTTP');`. Useful for debugging httpfs or S3 requests.

Storages:
- `memory` (default), `stdout` (CSV format), `file` (CSV).
- `CALL enable_logging(storage = 'stdout');`
- `CALL enable_logging(storage = 'file', storage_config = {'path': 'path/to/logs'});` or shorthand `storage_path = '...'`. Passing only `storage_config` or `storage_path` implies `storage = 'file'`.
- `duckdb_logs` follows the active storage, so switching storage changes what it returns.

Normalized vs denormalized (file storage): `memory` is normalized, `stdout` is not, `file` is configurable. Denormalized is generally recommended for file logging (faster, smaller logs). Per the docs example, `storage_path = '/tmp'` creates `duckdb_log_contexts.csv` and `duckdb_log_entries.csv` (normalized) while `storage_path = '/tmp/logs.csv'` creates one file (denormalized). The page's prose describing which spelling is which contradicts its own example, so check the files produced. `duckdb_logs` joins normalized tables so both read identically.

Buffering: logs are buffered (default 2048 entries for memory and file, 0 for stdout), so the last messages before a crash may be lost. For crash debugging use `storage_buffer_size = 0`, e.g. `CALL enable_logging(storage_path = '/tmp/mylogs', storage_buffer_size = 0);`. For fast stdout logging set `storage_buffer_size = 2048` (docs say over 10x faster).

## Checked

2026-11-07. Read the DuckDB 1.4 docs page operations_manual/logging/overview.md in full. Confirmed: enable/disable/truncate calls, levels and the INFO default, log types and the structured `duckdb_logs_parsed` macro, storages, shorthand parameters, default buffer sizes (2048 memory and file, 0 stdout), the over-10x stdout claim. Changed: the normalized/denormalized path rule now follows the page's example (the page prose contradicts it). Removed the invented Verify step.

Method: documentation only; no commands were run.
