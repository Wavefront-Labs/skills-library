---
id: computing-software.database-administration.duckdb.duckdb-securing-duckdb
name: duckdb-securing-duckdb
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, security, extensions, enable-external-access, lock-configuration, sandboxing]
level: practitioner
status: docs-checked
description: "Harden DuckDB: untrusted SQL, disabling file access, allowed_directories, extension signature levels, lock_configuration, secrets, resource limits."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/securing_duckdb/overview.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/securing_duckdb/securing_extensions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run DuckDB safely when data is sensitive or users are not fully trusted.

Principle: SQL in DuckDB is code, run with the full privileges of the process (read files, use network, load extensions). Untrusted SQL needs real sandboxing (duckdb-wasm, restricted container, VM, OS sandbox, network isolation, app-level query timeouts). The settings below are defense-in-depth, not a substitute. Non-SQL APIs (Python relational API, `read_csv(path)`, filter expressions) also read files and may accept subqueries, so validate their input too.

Hardening sequence (the docs give each setting separately; run `lock_configuration` last, after your own configuration is finished):

```sql
SET autoinstall_known_extensions = false;
SET autoload_known_extensions = false;
SET allow_community_extensions = false;
SET allowed_directories = ['/data/exports'];   -- optional fine-grained access
SET enable_external_access = false;             -- no ATTACH of files, COPY to/from files, read_csv/parquet/json of external sources
SET threads = 4;  SET memory_limit = '4GB';  SET max_temp_directory_size = '4GB';
SET lock_configuration = true;                   -- last: nothing can change afterward
```
- `SET disabled_filesystems = 'LocalFileSystem';` disables one file system instead of everything.
- With `allowed_directories = ['/tmp']` and `enable_external_access = false`, reading `test.csv` from the working directory fails with `Permission Error: Cannot access file "test.csv" - file system operations are disabled by configuration`. `allowed_paths` does the same for individual files.
- Security settings lock themselves: after `SET allow_community_extensions = false` you cannot set it back (`Cannot upgrade allow_community_extensions setting while database is running`). Resource settings do not self-lock, hence `lock_configuration`.
- CLI: `duckdb -safe ...` or `.safe_mode` (see duckdb-cli-arguments-safe-mode).

Extension trust levels (signature checked on every load): `core` key only (`allow_community_extensions = false`); `core` + `community` (default); any including unsigned (`allow_unsigned_extensions = true`, only settable at startup, for extension development). Community extensions are source-available and built/signed by the DuckDB team but not reviewed, so they execute third-party code; disable them in services that run user SQL.

Secrets: `duckdb_secrets()` redacts keys by default; keep `allow_unredacted_secrets` off for untrusted SQL. Queries can use any defined secret (temporary or persistent), so a write-capable S3 secret lets queries write the bucket. Persistent secrets are stored unencrypted on disk with owner-only permission (600).

SQL injection: use prepared statements for values (`execute("... WHERE x = ?", [42])`), never string concatenation. They protect only when you control the query structure.

Do not run DuckDB as root.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages operations_manual/securing_duckdb/overview.md and securing_extensions.md in full. Confirmed: SQL-as-code principle and sandboxing list, non-SQL API warning, defense-in-depth wording, every setting shown (autoload/autoinstall, allow_community_extensions, allowed_directories, enable_external_access and its three implications, disabled_filesystems, lock_configuration, threads, memory_limit, max_temp_directory_size), the permission error text, the self-locking error text, safe mode, the three signature levels and their configuration, community extension model, allow_unsigned_extensions at start-up, secrets redaction and `allow_unredacted_secrets`, write-capable secrets, owner-only `600` permission, prepared statements, no root. Changed: dropped the claim that the settings must run in a fixed order (the docs only say to lock after your own configuration), made the permission error context explicit, added `allowed_paths`, removed the invented Verify step (including the unconfirmed claim that re-enabling external access errors).

Method: documentation only; no commands were run.
