---
id: computing-software.database-administration.dragonfly.cache-mode-and-stick
name: cache-mode-and-stick
category: computing-software
field: database-administration
product: dragonfly
tags: [cache-mode, eviction, stick, maxmemory, dragonfly]
level: practitioner
status: docs-checked
description: "Run Dragonfly as an evicting cache with --cache_mode and exempt keys from eviction with STICK, plus the eviction tuning flags."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/generic/stick.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start with `--cache_mode` (with a `maxmemory` limit) and Dragonfly evicts items when it nears the memory limit instead of rejecting writes.

`STICK key [key ...]` (Dragonfly-specific) marks keys so they are not evicted in cache mode. Use it for must-keep entries in an otherwise evictable cache.

Eviction tuning flags (defaults):

| Flag | Default |
| --- | --- |
| `enable_heartbeat_eviction` | true |
| `max_eviction_per_heartbeat` | 100 |
| `max_segment_to_consider` | 4 |
| `eviction_memory_budget_threshold` | 0.1 |

Monitor with `evicted_keys` in `INFO stats` or `dragonfly_evicted_keys_total` in `/metrics`.

## Checked

2026-11-04. Confirmed in the flags page (`cache_mode` and the four eviction flags with defaults), the STICK page (cache mode, Dragonfly-specific) and the Monitoring page (`dragonfly_evicted_keys_total`). Nothing removed.

Method: documentation only; no commands were run.
