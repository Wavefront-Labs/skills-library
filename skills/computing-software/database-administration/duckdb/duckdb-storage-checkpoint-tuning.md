---
id: computing-software.database-administration.duckdb.duckdb-storage-checkpoint-tuning
name: duckdb-storage-checkpoint-tuning
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, pragma, checkpoint, compression, block-size, temp-directory, memory-limit]
level: advanced
status: docs-checked
description: "Tune DuckDB storage and resources: memory_limit caveats, threads, checkpoint and compression pragmas, temp_directory spilling, block size limits."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/configuration/pragmas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control memory, spill-to-disk, compression and checkpoint behaviour deliberately.

Memory and threads:

```sql
SET memory_limit = '1GB';
SET threads = 4;
```
Warning: `memory_limit` only bounds the buffer manager. Vectors, query results and aggregates with complex state (`list`, `mode`, `quantile`, `string_agg`, `approx` functions) allocate outside it, so real usage can exceed the limit.

Spilling: larger-than-memory operators spill to `<database_file_name>.tmp` next to the database file by default. Relocate with `SET temp_directory = '/path/to/temp_dir.tmp/';`.

Checkpointing and compression (applied at checkpoint, when column data and new changes are compressed):

```sql
PRAGMA force_compression = 'bitpacking';              -- prefer this codec where possible
PRAGMA disabled_compression_methods = 'fsst,rle';     -- comma-separated avoid list
PRAGMA force_checkpoint;                              -- make CHECKPOINT run even with no changes
PRAGMA enable_checkpoint_on_shutdown;                 -- checkpoint on clean shutdown and delete the WAL, leaving one file
PRAGMA disable_checkpoint_on_shutdown;
```

Block size: a database file is a list of blocks. The default is 262144 bytes (256 kB), which may be wasteful for tiny databases. Valid values are a power of two, at least 16384 and at most 262144:

```sql
SET default_block_size = '16384';   -- applies to new database files only
```
It can also be set per file in `ATTACH`.

Other behaviour switches in this area: `SET default_collation = 'nocase';`, `SET default_null_order = 'NULLS_LAST_ON_ASC_FIRST_ON_DESC';` (also `NULLS_FIRST`, `NULLS_LAST`, `NULLS_FIRST_ON_ASC_LAST_ON_DESC`), `SET default_order = 'DESCENDING';`, `SET ieee_floating_point_ops = false;` (then `1.0 / 0.0`, `0.0 / 0.0`, `-1.0 / 0.0` return NULL), `SET old_implicit_casting = true;` (pre-0.10.0 implicit casts to VARCHAR), `SET python_scan_all_frames = true;` (pre-1.1.0 Python replacement-scan behaviour).

Inspect: `PRAGMA database_size;` returns block size, free blocks and WAL size; `PRAGMA storage_info('t');` returns the `compression` per segment (see duckdb-pragma-metadata-introspection).

## Checked

2026-11-07. Read the DuckDB 1.4 docs page configuration/pragmas.md in full. Confirmed: memory_limit warning and the list of complex-state aggregates, threads, temp_directory default and override, force_compression, disabled_compression_methods, force_checkpoint, checkpoint on shutdown and WAL deletion, block size default, limits and per-file ATTACH option, default_collation, default_null_order values, default_order, ieee_floating_point_ops, old_implicit_casting, python_scan_all_frames, the `database_size` and `storage_info` output columns. Changed: removed the invented Verify wording in favour of a plain description of what those two pragmas return.

Method: documentation only; no commands were run.
