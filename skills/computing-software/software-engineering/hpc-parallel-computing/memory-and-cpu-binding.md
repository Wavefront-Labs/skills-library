---
id: computing-software.software-engineering.hpc-parallel-computing.memory-and-cpu-binding
name: memory-and-cpu-binding
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mem-per-cpu, cpu-bind, hint-nomultithread, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Placement"
sources: ["https://slurm.schedmd.com/sbatch.html", "https://slurm.schedmd.com/srun.html", "https://slurm.schedmd.com/cgroup.conf.html", "https://slurm.schedmd.com/sacct.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory, CPUs and binding

Goal: request memory and place tasks.
- `--mem=64G` is per node; `--mem-per-cpu` is per CPU. With `task/cgroup` and `ConstrainRAMSpace`, exceeding the limit triggers a kernel OOM event.
- `srun --cpu-bind=cores`, `--hint=nomultithread`, `--distribution=block:cyclic`.
- Check peak memory with `sacct -j <jobid> --format=JobID,MaxRSS,Elapsed`.
Verify: `MaxRSS` is below the requested memory.

## Checked

2026-11-03. Confirmed against the official pages: --mem, --mem-per-cpu, --hint=nomultithread, --distribution, srun --cpu-bind, ConstrainRAMSpace OOM note, sacct MaxRSS/Elapsed. Removed: seff (not in the Slurm documentation read; replaced by sacct fields).

Method: documentation only; no commands were run.
