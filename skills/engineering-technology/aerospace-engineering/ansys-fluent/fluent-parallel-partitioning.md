---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-parallel-partitioning
name: fluent-parallel-partitioning
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-hpc, parallel-partitioning, load-balancing, metis, cells-per-core, scaling]
level: practitioner
status: draft
description: "Partition meshes and balance load for parallel Fluent runs, check speed-up, and pick core counts based on cells per core."
sources:
  - "Ansys Fluent user guide (parallel processing)"
  - "Fluent TUI reference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: parallel partitioning

**Goal:** efficient use of cores.

## Practice
- Fluent partitions automatically on read; partition method options include Metis (default for most cases) and Cartesian-axis based methods.
- Rule of thumb: keep at least about 50,000-100,000 cells per core for good efficiency; too few cells per core means communication dominates (use scaling tests to confirm for your case).
- Check **Parallel > Partitioning and Load Balancing:** look at cell and interface counts per partition; imbalance above roughly 10% suggests rebalancing.
- Use `/parallel/timer/usage` to see where time is spent (communication vs compute), and `/parallel/partition/...` commands for rebalancing.
- Use double precision (`3ddp`) for compressible aerodynamics; single precision is faster but risks accuracy loss.

## Procedure
1. Run 50 iterations on 1, 2, 4, 8, 16 cores and plot time per iteration; compute speed-up.
2. Choose the core count at the knee of the curve.
3. For multi-node runs, use a fast interconnect and an MPI setting appropriate for the cluster.

## Gotchas
- Dynamic mesh or adaption demands rebalancing.
- Hyperthreads do not give more real cores; use physical cores.

## Verify
- [ ] Speed-up curve recorded; efficiency above about 70% at the chosen core count.
