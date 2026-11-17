---
id: computing-software.database-administration.dragonfly.memory-arena-diagnostics
name: memory-arena-diagnostics
category: computing-software
field: database-administration
product: dragonfly
tags: [memory-arena, allocator, fragmentation-waste, mimalloc, dragonfly]
level: advanced
status: docs-checked
description: "Inspect per-thread allocator arena waste in Dragonfly with MEMORY ARENA, its SUMMARY, BACKING and SHOW forms and report columns."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/memory-arena.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`MEMORY ARENA` (Dragonfly-specific diagnostic, `@read`, `@slow`) reports allocator arena statistics by block size, showing where committed memory goes and how much is wasted in partially filled blocks.

Syntax:

```
MEMORY ARENA [SUMMARY] [BACKING] [thread-id]
MEMORY ARENA SHOW
```

Each thread has its own heap, so the default reports thread `0`; pass a `thread-id` for another.

- `SUMMARY`: every thread in turn plus a machine-wide total, aggregated by block size, with `Wasted` (committed minus used) and `Waste%`. A `thread-id` cannot be combined with it.
- `BACKING`: reports the backing heap used for the server's own bookkeeping instead of the user data heap.
- `SHOW`: prints a process-wide report to the server's standard output and replies `OK`; it only prints if the server was started with `MIMALLOC_VERBOSE=1`. No further arguments allowed.

Default columns: `Count`, `BlockSize`, `Reserved`, `Committed`, `Used`. The report ends with totals and a `fragmentation waste` percentage.

Errors: a `thread-id` not below the thread count returns `Thread id must be less than N`; extra arguments after `SUMMARY` or `SHOW` return a syntax error.

See also `MEMORY DEFRAGMENT`.

## Checked

2026-11-04. Confirmed against the Dragonfly MEMORY ARENA page: syntax, ACL categories, Dragonfly-specific, thread 0 default, SUMMARY, BACKING and SHOW behaviour, columns, errors, fragmentation waste line. Removed the `INFO memory` pairing, which the page does not state.

Method: documentation only; no commands were run.
