---
id: computing-software.database-administration.valkey.benchmarking-pitfalls-and-factors
name: benchmarking-pitfalls-and-factors
category: computing-software
field: database-administration
product: valkey
tags: [benchmark, performance-factors, numa, unix-socket, network-bandwidth, reproducibility, connections]
level: advanced
status: docs-checked
description: "What affects Valkey benchmark results: pipelining, client bottlenecks, network bandwidth, Unix sockets, NUMA, connection counts, allocators, and reproducibility rules."
sources:
  - https://valkey.io/topics/benchmark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compare like with like: versions or options of Valkey on one workload. Do not compare with embedded stores, one-way stores or transactional databases (enable AOF with a chosen fsync policy if you do). Naive synchronous loops measure network and client latency, not Valkey. Command execution is essentially single-threaded; use several instances for multi-core scaling. By default `valkey-benchmark` uses concurrency only (no pipelining or threads), so it is nearer to worst case; the client itself can be the bottleneck.

Factors:
- Network: check with `ping`. 4 KB values at 100000 q/s need 3.2 Gbit/s, fine on 10 Gbit/s, not 1 Gbit/s.
- RAM speed matters little, except for objects over 10 KB.
- VMs run slower; real problems are over-provisioning, high-latency disks and old slow-`fork` hypervisors.
- Same host: Unix sockets can give about 50% more than TCP loopback, a gain that shrinks with long pipelines.
- Pipelined queries under the Ethernet packet size (about 1500 bytes) give nearly identical throughput for 10, 100 or 1000 bytes.
- NUMA: use `taskset` or `numactl`; best is client and server on different cores of one CPU sharing L3.
- Connections: more than 60000 benchmarked still sustaining 50000 q/s; 30000 connections give about half the throughput of 100.
- NIC queue affinity, RPS, jumbo frames; allocator (check `mem_allocator` in `INFO`).

Reproducibility: isolated hardware, fixed CPU frequency, enough RAM with no swap and correct `overcommit_memory`, no other I/O, RDB/AOF off NAS/NFS/EBS, `loglevel` warning or notice, avoid `MONITOR` (periodic `INFO` is fine).

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/benchmark/ (page text read in full): Apples-to-apples rule, embedded and one-way store caveats, AOF for transactional comparisons, naive synchronous loops, single-threaded execution, default concurrency-only behaviour, client bottleneck, 4 KB at 100000 q/s = 3.2 Gbit/s, >10 KB RAM note, VM causes, Unix sockets about 50%, ~1500-byte packet note, NUMA with taskset/numactl, 60000 and 30000 connection figures, NIC/RPS/jumbo frames, mem_allocator, reproducibility list.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
