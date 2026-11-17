---
id: computing-software.software-engineering.hpc-parallel-computing.cloud-vs-onprem-economics
name: cloud-vs-onprem-economics
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, hpc-cost-model, egress-costs, burst-to-cloud, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Cost"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud vs on-prem decisions

Goal: decide where to run.
- Compare utilisation, data gravity, egress, licence costs, queue wait.
- Burst to cloud for peaks; keep steady load on-prem.
- Measure real job cost per result.
Verify: decision documented with numbers.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
