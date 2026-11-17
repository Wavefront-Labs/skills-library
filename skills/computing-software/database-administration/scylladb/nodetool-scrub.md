---
id: computing-software.database-administration.scylladb.nodetool-scrub
name: nodetool-scrub
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, scrub, sstable-corruption, quarantine, segregate]
level: advanced
status: docs-checked
description: "nodetool scrub modes VALIDATE, ABORT, SKIP, SEGREGATE, quarantine modes, pre-scrub snapshot, and --drop-unfixable-sstables for repairing corrupted or out-of-order SSTables."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/scrub.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool scrub

`nodetool scrub [options] <keyspace> [<table...>]` helps identify and fix corrupted SSTables: it removes faulty data, drops tombstoned rows past `gc_grace`, and fixes out-of-order rows and partitions. Not every corruption can be fixed. By default a snapshot of the scrubbed tables is taken first; `-ns` / `--no-snapshot` skips it.

`-m` / `--mode` (default `VALIDATE`; overrides the deprecated `--skip-corrupted`):
- `VALIDATE`: read-only, reports corruption and checks stored digests; corrupt SSTables are moved to a `quarantine` subdirectory so compaction ignores them (`--quarantine-invalid-sstables true|false`, default true).
- `ABORT`: stop at the first validation error.
- `SKIP`: skip corrupt rows or partitions. Can lose data, even whole SSTables on digest mismatch.
- `SEGREGATE`: move out-of-order rows or partitions into additional SSTables.

`-q` / `--quarantine-mode`: `INCLUDE` (default, regular plus quarantined), `EXCLUDE` (regular only), `ONLY` (quarantined only).

`--drop-unfixable-sstables` (only with `--mode=SEGREGATE`) drops SSTables that cannot be fixed instead of aborting the whole scrub.

```
nodetool scrub mykeyspace mytable
nodetool scrub -m SEGREGATE mykeyspace mytable
nodetool scrub -m SEGREGATE --drop-unfixable-sstables mykeyspace mytable
```

Replacing the node is the only supported way to remove bad SSTables (the replacing node streams from other replicas, with no data-resurrection risk). The quarantine-and-drop alternative ends with `nodetool dropquarantinedsstables --i-accept-data-resurrection-risk` and can resurrect data; use it only when no viable alternative remains.

## Checked

2026-11-04: syntax, defaults, scrub and quarantine modes and the examples confirmed against the ScyllaDB nodetool scrub documentation page. Replaced the unsupported closing tip with the page's guidance on removing bad SSTables.

Method: documentation only; no commands were run.
