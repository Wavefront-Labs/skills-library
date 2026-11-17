---
id: computing-software.database-administration.dragonfly.tiering-metrics
name: tiering-metrics
category: computing-software
field: database-administration
product: dragonfly
tags: [info-tiered, tiered-pending-read, tiering-metrics, disk-bottleneck, dragonfly]
level: advanced
status: docs-checked
description: "Read INFO TIERED metrics on Dragonfly to see offloaded entries, disk usage, RAM hits and whether disk I/O is the bottleneck."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/tiering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run `INFO TIERED` to see the data tiering metrics:

| Metric | Meaning |
| --- | --- |
| `tiered_entries` | value entries offloaded to disk |
| `tiered_entries_bytes` | bytes offloaded |
| `tiered_total_stashes` | offload requests issued |
| `tiered_total_fetches` | times offloaded entries were read from disk |
| `tiered_total_deletes` | offloaded entries deleted from disk |
| `tiered_total_uploads` | offloaded entries promoted back to memory |
| `tiered_allocated_bytes` | disk space used |
| `tiered_capacity_bytes` | maximum on-disk capacity |
| `tiered_pending_read_cnt` | pending read I/O; high means read bottleneck |
| `tiered_pending_stash_cnt` | pending write I/O; high means write bottleneck |
| `tiered_cold_storage_bytes` | cooling queue capacity in bytes |
| `tiered_ram_hits` | lookups served from memory |
| `tiered_ram_misses` | lookups that read from disk |
| `tiered_ram_cool_hits` | lookups served from the cooling buffer |

Reading them:

- A growing `tiered_ram_misses` relative to `tiered_ram_hits` means more reads go to disk.
- Sustained high pending read or stash counts show the server is limited by disk I/O.
- Compare `tiered_allocated_bytes` with `tiered_capacity_bytes` for headroom.

In cluster mode, `DFLYCLUSTER GETSLOTINFO` reports bytes per slot on disk as `tiered_bytes`.

## Checked

2026-11-04. Confirmed in the SSD Data Tiering page (metrics list and descriptions, bottleneck wording) and the GETSLOTINFO page (`tiered_bytes`). The reading tips are interpretation of those fields. Nothing removed.

Method: documentation only; no commands were run.
