---
id: computing-software.software-engineering.hpc-parallel-computing.containers-mpi-and-slurm
name: containers-mpi-and-slurm
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, srun-apptainer, pyxis-enroot, hybrid-mpi-container, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Multi-node containers"
sources: ["https://apptainer.org/docs/user/latest/mpi.html", "https://github.com/NVIDIA/pyxis", "https://slurm.schedmd.com/containers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containerised MPI under Slurm

Goal: scale containers.
- Hybrid model: `srun apptainer exec app.sif ./mpi_app` with an MPI inside the image that supports the same process-management interface (PMI2/PMIx) and version as the launcher.
- Pyxis/Enroot: `srun --container-image=IMAGE` (needs the Pyxis plugin installed by the site); Slurm 21.08+ also has a native `--container` option for OCI bundles.
- If the containerised MPI lacks the PMI support that `srun` uses, the application will not start correctly.
Verify: a multi-node `srun` run of the containerised application completes.

## Checked

2026-11-03. Confirmed against the official pages: Apptainer MPI hybrid model with srun and PMI2/PMIx matching, Pyxis --container-image, Slurm --container (containers page). Removed: the InfiniBand-fabric test and bandwidth claims.

Method: documentation only; no commands were run.
