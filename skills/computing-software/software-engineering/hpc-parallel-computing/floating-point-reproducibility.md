---
id: computing-software.software-engineering.hpc-parallel-computing.floating-point-reproducibility
name: floating-point-reproducibility
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, bitwise-reproducibility, reduction-order, fused-multiply-add, floating-point-reproducibility, mixed-precision, verification-hpc, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Same answer every run"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Floating-point reproducibility

Goal: control numerical variation.
- Reduction order, FMA contraction, vector widths and thread counts change low-order bits.
- Use deterministic reductions or compensated sums (Kahan); compare with tolerances not equality.
- Record compiler flags and library versions.
Verify: results agree within a stated tolerance across configurations.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
