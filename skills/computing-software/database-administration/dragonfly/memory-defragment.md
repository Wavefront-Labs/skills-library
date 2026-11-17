---
id: computing-software.database-administration.dragonfly.memory-defragment
name: memory-defragment
category: computing-software
field: database-administration
product: dragonfly
tags: [memory-defragment, defrag, fragmentation, mem-defrag-threshold, dragonfly]
level: advanced
status: docs-checked
description: "Reclaim fragmented Dragonfly memory with MEMORY DEFRAGMENT, its threshold, incremental scan behaviour, report fields and background defrag flags."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/memory-defragment.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`MEMORY DEFRAGMENT [threshold]` (Dragonfly-specific) runs defragmentation on demand and returns a report. After deleting many keys, `used_memory_rss` in `INFO` can stay high because pages are only sparsely used; defragmentation relocates objects off such pages so the allocator can release them.

Background task flags: `mem_defrag_threshold` (0.7, minimum used/maxmemory), `mem_defrag_waste_threshold` (0.2, wasted/committed) and `mem_defrag_check_sec_interval` (60). The command runs the same logic immediately without those gates.

`threshold` is a ratio between 0 and 1: a page is relocated if used/capacity is below it. Default is `mem_defrag_page_utilization_threshold` (0.8). Raise it to be more aggressive. Invalid floats return `ERR value is not a valid float`.

Behaviour:

- Runs on every shard thread in parallel, each with a small time budget, so one call scans only part of the keyspace. Each shard keeps a cursor; call repeatedly to cover everything.
- A shard that finished a pass reports an empty section on the next call, then restarts.
- It may monopolise shard threads, causing high CPU and latency spikes. Run in low-traffic periods.

Report fields include `Pages scanned`, `Pages marked for reallocation`, `Pages full` and per-shard block usage. Cumulative progress is in `defrag_attempt_total`, `defrag_realloc_total`, `defrag_task_invocation_total`.

## Checked

2026-11-04. Confirmed against the Dragonfly MEMORY DEFRAGMENT page and the flags page: threshold ratio and its 0.8 default via `mem_defrag_page_utilization_threshold`, background flag defaults 0.7, 0.2 and 60, incremental per-shard cursors, empty section after a completed pass, CPU and latency warning, report fields, float error, cumulative INFO counters. Nothing removed.

Method: documentation only; no commands were run.
