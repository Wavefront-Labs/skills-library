---
id: computing-software.software-engineering.hpc-parallel-computing.node-numa-topology
name: node-numa-topology
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, hwloc, lstopo, numa-topology, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "CPU and memory layout"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Node hardware topology

Goal: read a node.
- `lscpu`, `numactl -H`, `lstopo`; sockets, NUMA domains, caches, GPUs and NIC locality.
- Bind ranks near their NIC/GPU.
- Hyper-threads often disabled in HPC runs.
Verify: placement matches locality.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
