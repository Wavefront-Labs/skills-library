---
id: computing-software.software-engineering.hpc-parallel-computing.kokkos-sycl-portability
name: kokkos-sycl-portability
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, kokkos-parallel-for, sycl-queue, performance-portability, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Performance portability"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kokkos and SYCL

Goal: single-source GPU/CPU code.
- Kokkos: `Kokkos::parallel_for("name", N, KOKKOS_LAMBDA(int i){...})`, Views with memory spaces.
- SYCL: queues, buffers/USM, `parallel_for`.
- Pick based on target systems and ecosystem (confirm support).
Verify: same code builds and passes tests on CPU and GPU backends.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
