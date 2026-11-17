---
id: computing-software.software-engineering.hpc-parallel-computing.interconnects-and-topology
name: interconnects-and-topology
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, infiniband-fabric, fat-tree, dragonfly, infiniband, interconnect, node-architecture, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Network basics"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interconnects and topology

Goal: understand the network.
- InfiniBand/Slingshot/Omni-Path; fat-tree and dragonfly topologies; latency vs bandwidth.
- Tools: `ibstat`, `ibv_devinfo`, `ib_write_bw`, `osu_latency`.
- Placement on the same switch matters for latency-sensitive jobs.
Verify: point-to-point bandwidth near line rate.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
