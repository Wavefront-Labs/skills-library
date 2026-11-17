---
id: computing-software.software-engineering.hpc-parallel-computing.apptainer-usage
name: apptainer-usage
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, apptainer-build, apptainer-exec, sif-image, apptainer, singularity, enroot, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Rootless containers"
sources: ["https://apptainer.org/docs/user/latest/build_a_container.html", "https://apptainer.org/docs/user/latest/gpu.html", "https://apptainer.org/docs/user/latest/bind_paths_and_mounts.html", "https://apptainer.org/docs/user/latest/mpi.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apptainer (Singularity)

Goal: run containers on clusters.
- `apptainer build app.sif docker://ubuntu:22.04`, `apptainer exec --nv app.sif python train.py` (`--nv` for NVIDIA GPUs, `--rocm` for AMD).
- Bind host paths with `--bind /scratch:/scratch`.
- For MPI use the host-MPI bind model or the hybrid model (the MPI inside the container must be compatible with the host launcher).
Verify: container sees GPUs and scratch.

## Checked

2026-11-03. Confirmed against the official pages: apptainer build from docker://, exec, --nv, --rocm, --bind, the bind and hybrid MPI models. Removed: nothing removed.

Method: documentation only; no commands were run.
