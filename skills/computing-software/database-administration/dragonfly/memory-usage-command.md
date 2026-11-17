---
id: computing-software.database-administration.dragonfly.memory-usage-command
name: memory-usage-command
category: computing-software
field: database-administration
product: dragonfly
tags: [memory-usage, memory-stats, withoutkey, dragonfly]
level: intro
status: docs-checked
description: "Measure a key's memory with MEMORY USAGE (including WITHOUTKEY and inline-value zeros) and connection memory with MEMORY STATS."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/memory-usage.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/memory-stats.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## MEMORY USAGE

```
MEMORY USAGE key [WITHOUTKEY]
```

Returns bytes needed to store the value at `key`, including the key itself. O(1) for strings and O(N) for collections.

- `WITHOUTKEY` (Dragonfly-specific) counts only the value; the difference matters with long key names.
- Small values stored inline in the key table have no separate allocation, so the command reports `0` for them (the docs show `abc` reporting `0`).
- The Redis `SAMPLES` option is not supported; extra arguments after the key are ignored, so `MEMORY USAGE key SAMPLES 0` behaves like `MEMORY USAGE key`.
- A missing key returns nil.

## MEMORY STATS

Reports connection memory only, as a map:

| Field | Meaning |
| --- | --- |
| `connections.direct_bytes` | bytes for client connections, excluding replication |
| `replication.connections_count` | connections serving a replication flow |
| `replication.direct_bytes` | bytes for those replication connections |

It does not mirror Redis's larger field set. For overall memory use the `memory` section of `INFO`; for allocator internals use `MEMORY MALLOC-STATS` or `MEMORY ARENA`.

## Checked

2026-11-04. Confirmed against the Dragonfly MEMORY USAGE and MEMORY STATS pages: syntax, complexity, `WITHOUTKEY`, inline values reporting 0, `SAMPLES` unsupported and extra arguments ignored, nil for a missing key, the three MEMORY STATS fields, and the pointers to INFO, MEMORY MALLOC-STATS and MEMORY ARENA. Nothing removed.

Method: documentation only; no commands were run.
