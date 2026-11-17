---
id: computing-software.software-engineering.hpc-parallel-computing.cloud-cluster-deployment
name: cloud-cluster-deployment
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, aws-parallelcluster, slurm-cloud, spot-instances, cloud-hpc, parallelcluster, efa, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Elastic clusters"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud HPC clusters

Goal: stand up a cloud cluster.
- ParallelCluster/CycleCloud create Slurm clusters with auto-scaling queues; use placement groups and EFA/InfiniBand instance types.
- Use spot with checkpointing; keep data close to compute.
- Cost guardrails (budgets, max nodes).
Verify: scaling up/down matches queue demand.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
