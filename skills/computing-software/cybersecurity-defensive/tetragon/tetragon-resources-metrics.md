---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-resources-metrics
name: tetragon-resources-metrics
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [metrics-resources]
level: advanced
status: docs-checked
description: "Reference for the Go runtime and process resource metrics (go_* and process_*) that the Tetragon agent exposes."
sources:
  - "https://tetragon.io/docs/reference/metrics/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon resources metrics

Goal: find the metric that shows how much CPU, memory, file descriptors or network the Tetragon agent itself uses. The metrics reference lists them under "Tetragon Resources Metrics".

## Process

- `process_cpu_seconds_total`: user and system CPU time in seconds.
- `process_resident_memory_bytes`: resident memory; `process_virtual_memory_bytes` and `process_virtual_memory_max_bytes`: virtual memory used and available.
- `process_open_fds` and `process_max_fds`: open and maximum file descriptors.
- `process_network_receive_bytes_total` and `process_network_transmit_bytes_total`: bytes received and sent over the network.
- `process_start_time_seconds`: start time since the unix epoch.

## Go runtime

- Scheduler: `go_goroutines` (existing goroutines), `go_threads` (OS threads created), `go_sched_gomaxprocs_threads` (current GOMAXPROCS), `go_sched_latencies_seconds` (time goroutines spend runnable before running).
- GC: `go_gc_duration_seconds` (stop-the-world pause summary), `go_gc_gogc_percent` (heap target percentage, otherwise 100), `go_gc_gomemlimit_bytes` (memory limit, otherwise math.MaxInt64), `go_memstats_last_gc_time_seconds`, `go_memstats_next_gc_bytes` (heap size at next GC).
- Heap: `go_memstats_alloc_bytes` (heap bytes in use, same as `go_memstats_heap_alloc_bytes`), `go_memstats_alloc_bytes_total`, `go_memstats_heap_inuse_bytes`, `go_memstats_heap_idle_bytes`, `go_memstats_heap_released_bytes`, `go_memstats_heap_sys_bytes`, `go_memstats_heap_objects`, `go_memstats_mallocs_total`, `go_memstats_frees_total`.
- Other memory: `go_memstats_stack_inuse_bytes`, `go_memstats_stack_sys_bytes`, `go_memstats_mcache_*`, `go_memstats_mspan_*`, `go_memstats_gc_sys_bytes`, `go_memstats_buck_hash_sys_bytes`, `go_memstats_other_sys_bytes`, and `go_memstats_sys_bytes` (total obtained from the system).
- `go_info`: Go environment information (label `version`).

## Checked

2026-11-08. Read in full: the Tetragon metrics reference (raw markdown `docs/content/en/docs/reference/metrics.md`, section "Tetragon Resources Metrics"). Every metric name and description above matches. Removed the unsourced claim about collectors and endpoint.

Method: documentation only; no commands were run.
