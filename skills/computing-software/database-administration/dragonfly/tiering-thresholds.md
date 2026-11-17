---
id: computing-software.database-administration.dragonfly.tiering-thresholds
name: tiering-thresholds
category: computing-software
field: database-administration
product: dragonfly
tags: [tiered-offload-threshold, tiered-upload-threshold, tiered-min-value-size, experimental-cooling, dragonfly]
level: advanced
status: docs-checked
description: "Tune Dragonfly tiering with offload and upload thresholds, minimum value size, pending stash bytes and experimental cooling."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/tiering.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flags (defaults from the flag reference):

| Flag | Meaning | Default |
| --- | --- | --- |
| `tiered_offload_threshold` | free-memory ratio below which values are actively offloaded in the background | 0.5 |
| `tiered_upload_threshold` | free-memory ratio below which values read from disk are no longer promoted to memory | 0.1 |
| `tiered_min_value_size` | minimum value size to offload; at least 64 | 64 |
| `tiered_max_pending_stash_bytes` | max bytes in flight to disk before stashes are rejected or backpressure applies | 256.0KiB |
| `tiered_min_ttl_to_offload_ms` | minimum remaining TTL for offloading | 5000 |
| `tiered_experimental_cooling` | keep an in-memory copy too | true |

Worked example from the docs with `--maxmemory=20G --tiered_upload_threshold=0.2 --tiered_offload_threshold=0.4`:

- Above 16GB used (less than 20% free): values read from disk go to the client without promotion to memory.
- Active background offloading starts at 12GB used (less than 40% free).
- Between 12GB and 16GB, continuous upload/offload keeps recently used entries in memory.

Cooling: with `tiered_experimental_cooling` a copy stays in memory, so entries change state without pending I/O. These duplicates count in both `tiered_entries_bytes` and `used_memory`, but thresholds ignore them. Real free memory is `used_memory` minus `tiered_cold_storage_bytes`.

Retired flag: `tiered_storage_write_depth` was replaced by `tiered_max_pending_stash_bytes`.

## Checked

2026-11-04. Confirmed in the SSD Data Tiering page (thresholds, worked example, cooling accounting, retired flag) and the flags page (defaults for each flag in the table). Corrected the `tiered_experimental_cooling` default, which the flags page gives as true, not off.

Method: documentation only; no commands were run.
