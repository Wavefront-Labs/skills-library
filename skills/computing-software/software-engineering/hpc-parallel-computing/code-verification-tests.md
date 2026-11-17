---
id: computing-software.software-engineering.hpc-parallel-computing.code-verification-tests
name: code-verification-tests
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, unit-tests-hpc, method-of-manufactured-solutions, regression-baseline, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Testing scientific codes"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verification and regression tests

Goal: trust results.
- Convergence-order tests, manufactured solutions, conservation checks, baseline comparisons in CI on small runs.
- Run tests under MPI with multiple rank counts.
- Keep tolerance policy documented.
Verify: CI fails on a deliberate bug.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
