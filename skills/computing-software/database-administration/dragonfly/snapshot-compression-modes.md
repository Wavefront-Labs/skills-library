---
id: computing-software.database-administration.dragonfly.snapshot-compression-modes
name: snapshot-compression-modes
category: computing-software
field: database-administration
product: dragonfly
tags: [compression-mode, compression-level, snapshot-egress, serialization, dragonfly]
level: advanced
status: docs-checked
description: "Choose Dragonfly snapshot compression with compression_mode and compression_level, and cap snapshot network egress per shard."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flags from the Dragonfly flag reference:

`--compression_mode` (default `3`) selects the snapshot compression:

| Value | Name | Behaviour |
| --- | --- | --- |
| 0 | NONE | no compression |
| 1 | SINGLE_ENTRY | single-entry LZF compression |
| 2 | MULTI_ENTRY_ZSTD | multi-entry ZSTD for Dragonfly snapshots, single-entry for RDB |
| 3 | MULTI_ENTRY_LZ4 | multi-entry LZ4 for Dragonfly snapshots, single-entry for RDB |

`--compression_level` (default `2`) is the level used for zstd/lz4 compression.

`--snapshot_egress_limit_bytes` (default `0B`; a value of 0 disables throttling) is a per-shard-thread socket egress bandwidth budget in bytes per second. Each shard throttles its snapshot traversal loop to stay under the rate. Human-readable sizes such as `100mb` and `1gb` are accepted.

`--serialization_max_chunk_size` (default 65536) sets the largest value serialised at once during snapshotting or full sync; bigger values use streaming serialisation, and `0` disables streaming mode.

`--df_snapshot_format` (default true): if true, save in the Dragonfly-specific snapshotting format.

## Checked

2026-11-04. Confirmed against the Dragonfly flags page: all five flags, their defaults, the four compression modes, the 100mb and 1gb sizes, streaming serialisation with 0 disabling it. Nothing removed.

Method: documentation only; no commands were run.
