---
id: computing-software.database-administration.duckdb.duckdb-configuration-settings
name: duckdb-configuration-settings
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, configuration, set, reset, memory-limit, threads, settings]
level: practitioner
status: docs-checked
description: "Set, reset and inspect DuckDB settings (SET, RESET, current_setting, duckdb_settings) and the main options for memory, threads, temp files, caches and HTTP."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/configuration/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change and verify DuckDB behaviour through configuration options.

Mechanics: `SET name = value;` or `SET name TO value;` (also `PRAGMA`), undo with `RESET name;`. Read with `SELECT current_setting('memory_limit');` or `FROM duckdb_settings() WHERE name = 'threads'` (columns name, value, description, input_type, scope). Options have a default scope, GLOBAL or LOCAL.

```sql
SET memory_limit = '10GB';
SET threads TO 1;
SET enable_progress_bar = true;
SET default_null_order = 'nulls_last';
RESET memory_limit;
```

Resources (global): `memory_limit`/`max_memory` (default 80% of RAM), `threads`/`worker_threads` (default CPU cores), `temp_directory` (default `<database_name>.tmp`, or `.tmp` in memory mode), `max_temp_directory_size` (default 90% of available disk), `temp_file_encryption` (false), `checkpoint_threshold`/`wal_autocheckpoint` (default 16 MiB WAL), `preserve_insertion_order` (true; if false the system may re-order results that have no ORDER BY), `allocator_flush_threshold` (128 MiB).

Access and safety (global): `enable_external_access` (true; false blocks file and module access), `allowed_directories`, `allowed_paths`, `disabled_filesystems`, `allow_community_extensions` (true), `allow_unsigned_extensions` (false), `autoinstall_known_extensions` and `autoload_known_extensions` (true), `lock_configuration` (false), `access_mode` (`automatic`, `read_only`, `read_write`). See duckdb-securing-duckdb.

Remote I/O: `http_timeout` 30 s, `http_retries` 3, `http_retry_wait_ms` 100, `http_retry_backoff` 4, `http_keep_alive` true, `http_proxy*`, `ca_cert_file`, `enable_server_cert_verification`, `enable_external_file_cache` true, `parquet_metadata_cache` false, `s3_*` settings, `partitioned_write_max_open_files` 100.

Local options: `enable_profiling` (`JSON`, `QUERY_TREE`, `QUERY_TREE_OPTIMIZER`), `profiling_mode` (STANDARD/DETAILED), `profile_output`, `explain_output` (`physical_only`), `enable_progress_bar`, `progress_bar_time` 2000 ms, `file_search_path`, `search_path`, `schema`, `max_expression_depth` 1000, `errors_as_json`, `lambda_syntax`.

Logging: `enable_logging`, `logging_level` (INFO), `logging_mode`, `logging_storage` (memory); see duckdb-logging.

Check an option's default scope (GLOBAL or LOCAL) in the `scope` column of `duckdb_settings()`.

## Checked

2026-11-07. Read the Configuration page in full, including the global and local option tables, and confirmed the SET, PRAGMA, RESET, `current_setting` and `duckdb_settings()` mechanics and columns, and every default and name quoted for resources, access and safety, remote I/O, local options and logging. Removed an unsupported claim that extension options must be set before the extension loads, an unsupported 'save memory' purpose for `preserve_insertion_order`, the word 'legacy' for `s3_*` settings, and the Verify step.

Method: documentation only; no commands were run.
