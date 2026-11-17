---
id: computing-software.database-administration.duckdb.duckdb-limits-files-and-space
name: duckdb-limits-files-and-space
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, limits, wal, tmp, gitignore, checkpoint, reclaim-space, compaction]
level: practitioner
status: docs-checked
description: "DuckDB built-in limits, files it creates (.wal, .tmp, home-directory files), gitignore patterns, reclaiming disk space, non-deterministic result ordering."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/limits.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/footprint_of_duckdb/files_created_by_duckdb.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/footprint_of_duckdb/gitignore_for_duckdb.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/footprint_of_duckdb/reclaiming_space.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/operations_manual/non-deterministic_behavior.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know DuckDB's limits and on-disk footprint, shrink files, and get repeatable results.

Limits (check yours with `current_setting('name')`): array size 100000; BLOB 4 GB; string 4 GB; expression depth 1000 (`max_expression_depth`); memory 80% of RAM (`memory_limit`, applies to the buffer manager only); temp directory unlimited (`max_temp_directory_size`); vector allocation 128 GB. No practical database file size limit (15 TB+ files work), but connecting may take a few seconds and checkpointing can be slower.

Files created:
- Home directory (global): `~/.duckdbrc` (CLI startup commands, dot or SQL), `~/.duckdb_history` (CLI), `~/.duckdb/extensions` (installed extensions, per DuckDB version), `~/.duckdb/stored_secrets` (persistent secrets).
- Next to the database (on-disk mode): `<db>` (any extension: `.duckdb`, `.db`, `.ddb`), `<db>.tmp/` (spill directory), `<db>.wal`. In-memory mode uses `.tmp/` in the working directory.
- The WAL is deleted on clean exit; after a crash it is required to recover data.

Gitignore: keep the database but ignore scratch with `*.wal` and `*.tmp/`; ignore the database too by adding `*.duckdb*` (match your extension).

Reclaiming space (single-file format): use `CHECKPOINT` to reclaim space after deleting rows. `VACUUM` does not reclaim space. To compact the database, create a fresh copy:

```sql
ATTACH 'db1.db' AS db1;
ATTACH 'db2.db' AS db2;
COPY FROM DATABASE db1 TO db2;
```

Non-determinism (expected behaviour): without `ORDER BY`, row order may vary between runs (set semantics, multi-threading); `array_distinct` order differs across platforms; floating-point aggregates such as `stddev` and `corr` can return small numbers (`0 <= z < 10e-16`) instead of 0 when run on multiple threads. To get stable results: `SET threads = 1;`, add `ORDER BY ALL`, sort lists with `list_sort(...)`, or shuffle deterministically.

## Checked

2026-11-07. Read the Limits, Files Created by DuckDB, Gitignore for DuckDB, Reclaiming Space and Non-Deterministic Behavior pages in full and confirmed the limit table values and options, the large-file note, the global and local file lists, WAL behaviour, both gitignore snippets, the VACUUM and COPY FROM DATABASE compaction steps and each non-determinism case with its workarounds. Reworded the large-file, WAL, reclaiming and floating-point sentences to the pages' wording (removed 'do not delete', 'only after' and 'fully', and used the page's numeric bound) and removed the Verify step.

Method: documentation only; no commands were run.
