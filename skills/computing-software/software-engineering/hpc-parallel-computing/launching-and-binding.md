---
id: computing-software.software-engineering.hpc-parallel-computing.launching-and-binding
name: launching-and-binding
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpirun-bind-to, srun-mpi, rank-placement, mpirun, mpiexec, process-binding, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Running MPI jobs"
sources: ["https://docs.open-mpi.org/en/main/man-openmpi/man1/mpirun.1.html", "https://slurm.schedmd.com/srun.html", "https://slurm.schedmd.com/cpu_management.html", "https://slurm.schedmd.com/mpi_guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Launching and process binding

Goal: place ranks well.
- `mpirun -n 64 --map-by ppr:32:node --bind-to core ./app` (Open MPI); `srun --cpu-bind=cores` under Slurm.
- Print binding: `--report-bindings` (Open MPI).
- Open MPI does not oversubscribe nodes by default (`--nooversubscribe`); `--oversubscribe` overrides this.
Verify: `--report-bindings` shows one rank per core.

## Checked

2026-11-03. Confirmed against the official pages: Open MPI --map-by ppr:N:node, --bind-to, --report-bindings, -n/-np and oversubscribe behaviour; srun --cpu-bind cores; srun launching with PMI. Removed: the MPICH -bind-to option (no MPICH page read) and the unsupported claim that oversubscription kills performance.

Method: documentation only; no commands were run.
