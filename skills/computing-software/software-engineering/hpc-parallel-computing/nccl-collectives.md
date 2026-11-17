---
id: computing-software.software-engineering.hpc-parallel-computing.nccl-collectives
name: nccl-collectives
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, nccl, nccl-allreduce, nvlink, multi-gpu, cuda-aware-mpi, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "GPU collectives"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NCCL collectives

Goal: communicate between GPUs.
- NCCL provides AllReduce, Broadcast, AllGather, ReduceScatter over NVLink/PCIe/InfiniBand; `ncclCommInitRank`.
- Debug with `NCCL_DEBUG=INFO`; tune `NCCL_IB_*`, `NCCL_SOCKET_IFNAME`.
- Test with nccl-tests (`all_reduce_perf`).
Verify: bus bandwidth near hardware limit.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
