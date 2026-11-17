---
id: computing-software.database-administration.dragonfly.info-memory-fields
name: info-memory-fields
category: computing-software
field: database-administration
product: dragonfly
tags: [info-memory, rss, used-memory, maxmemory, dragonfly]
level: practitioner
status: docs-checked
description: "Read Dragonfly INFO sections, compare used_memory with used_memory_rss to spot fragmentation, and parse INFO fields defensively."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/info.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`INFO [section ...]` returns `field:value` lines. Sections: `server`, `clients`, `memory`, `persistence`, `stats`, `replication`, `cpu`, `commandstats`, `latencystats`, `keyspace`, `errorstats`, or `all`. With no argument the output includes `memory` and `latencystats` but not `commandstats`.

Memory fields:

- `used_memory`: bytes allocated by Dragonfly via its allocator.
- `used_memory_peak`: peak consumption.
- `used_memory_rss`: bytes as the OS sees them (what `top` and `ps` show).
- `maxmemory`: the configured limit.

Rule of thumb from the docs: `used_memory_rss` should be only slightly higher than `used_memory`. When RSS is much greater, there may be external memory fragmentation. Memory freed by Dragonfly goes back to the allocator, which may not return it to the OS; check `used_memory_peak` too.

Other useful lines: `connected_clients`, `blocked_clients`, `instantaneous_ops_per_sec`, `expired_keys`, `evicted_keys`, `keyspace_hits`, `keyspace_misses`, `rejected_connections` (connections rejected because of the `maxclients` limit). The sample output also shows `defrag_attempt_total`, `defrag_realloc_total` and `defrag_task_invocation_total` in the stats section, without describing them.

Fields are added or removed between versions. Skip unknown properties and tolerate missing ones when parsing.

## Checked

2026-11-04: confirmed against the INFO command page (section list, default output, memory fields and the RSS rule of thumb, stats fields). Reworded the defrag counters, which the page lists only in sample output, and removed a cross-reference to another skill.
Method: documentation only; no commands were run.
