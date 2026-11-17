---
id: computing-software.software-engineering.hpc-parallel-computing.srun-and-interactive
name: srun-and-interactive
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, srun-pty, salloc, interactive-session, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Interactive work"
sources: ["https://slurm.schedmd.com/salloc.html", "https://slurm.schedmd.com/srun.html", "https://slurm.schedmd.com/mpi_guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# srun, salloc and interactive jobs

Goal: run interactively.
- `salloc -N1 -n4 -t 01:00:00` then `srun ./app`; `srun --pty bash` for a shell.
- Launch MPI with `srun` (PMI/PMIx) rather than `mpirun` where configured.
- Exiting the salloc shell relinquishes the allocation.
Verify: allocation shown in `squeue` and released at exit.

## Checked

2026-11-03. Confirmed against the official pages: salloc options and the relinquish-on-exit behaviour (salloc page), srun --pty (srun page), srun launching via PMI-1/PMI-2/PMIx (MPI guide). Removed: nothing removed.

Method: documentation only; no commands were run.
