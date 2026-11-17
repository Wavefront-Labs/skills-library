---
id: computing-software.software-engineering.concurrency.cpu-cache-misses-and-numa
name: cpu-cache-misses-and-numa
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, cache-misses, numa, perf-stat, false-sharing, memory-locality]
level: sme
status: draft
description: "Measure CPU cache misses and NUMA effects with perf, numastat and numactl, and fix locality problems: false sharing, remote memory access, thread and memory placement."
sources: ["https://perf.wiki.kernel.org/index.php/Tutorial", "https://man7.org/linux/man-pages/man8/numactl.8.html", "https://www.kernel.org/doc/html/latest/admin-guide/mm/numa_memory_policy.html", "https://www.brendangregg.com/perf.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPU cache misses and NUMA effects

## Measure cache behaviour
```
perf stat -e cycles,instructions,cache-references,cache-misses,L1-dcache-load-misses,LLC-load-misses ./app
perf stat -d -d ./app                 # detailed: L1/LLC/TLB events
perf record -e LLC-load-misses -g ./app && perf report     # where misses happen
perf c2c record ./app && perf c2c report                   # cache-line contention / false sharing
```
- **IPC** (instructions/cycle) < ~1 on a modern core often means memory stalls; > 2 is compute-bound.
- High LLC miss rate in a hot loop = poor locality (pointer chasing, large strides, random access).
- Top-down analysis: `perf stat --topdown` (Intel) or `toplev` (pmu-tools) classifies cycles as
  frontend-bound, backend/memory-bound, bad speculation, retiring.
Cloud VMs may not expose all PMU counters.

## Fix locality
- Contiguous arrays over linked structures; struct-of-arrays for hot fields; iterate in memory order
  (row-major in C, NumPy C-order).
- Smaller data types, packing hot fields together, splitting cold fields out.
- **False sharing**: threads writing different variables on the same 64-byte line. Pad/align
  (`alignas(64)`, Java `@Contended` with `-XX:-RestrictContended`, Rust `crossbeam::CachePadded`),
  or keep per-thread counters and merge.
- Huge pages (THP or explicit) for large working sets with TLB misses (`dTLB-load-misses`).

## NUMA
Multi-socket (and some single-socket chiplet) servers have memory local to each node; remote access
costs ~1.5-2x latency and shares interconnect bandwidth.
```
lscpu | grep -i numa ; numactl --hardware        # nodes, CPUs, distances
numastat -p <PID>                                # per-node memory of a process
perf stat -e node-load-misses,node-loads ./app
numactl --cpunodebind=0 --membind=0 ./app        # pin CPU and memory to node 0
numactl --interleave=all ./db                    # spread memory (big shared caches)
```
- Linux allocates on first touch: the thread that first writes a page decides its node. Initialise
  data on the threads that will use it.
- Automatic NUMA balancing (`kernel.numa_balancing`) migrates pages; can help or add overhead.
- JVM `-XX:+UseNUMA` (Parallel/G1); databases often recommend interleave or one instance per node.
- Containers/Kubernetes: CPU Manager `static` + Topology Manager `single-numa-node` for latency-
  critical pods.

## Verify
Compare IPC, LLC misses and wall time before/after; check remote vs local memory ratios in numastat.
