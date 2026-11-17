---
id: computing-software.software-engineering.hpc-parallel-computing.sbatch-scripts
name: sbatch-scripts
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, sbatch-directives, sbatch-ntasks, sbatch-time, slurm, sbatch, srun, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Batch jobs"
sources: ["https://slurm.schedmd.com/sbatch.html", "https://slurm.schedmd.com/sched_config.html", "https://slurm.schedmd.com/sacct.html", "https://slurm.schedmd.com/squeue.html", "https://slurm.schedmd.com/scancel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing sbatch scripts

Goal: submit reliable batch jobs.
- `#SBATCH --job-name=x --nodes=2 --ntasks-per-node=32 --cpus-per-task=1 --time=02:00:00 --partition=compute --output=%x-%j.out`.
- Submit with `sbatch job.sh`; inspect with `squeue -u $USER`; cancel with `scancel <jobid>`.
- Request only what you need; accurate `--time` helps backfill.
Verify: `sacct -j <id>` shows COMPLETED.

## Checked

2026-11-03. Confirmed against the official pages: the sbatch options, the %x/%j filename patterns, squeue -u, scancel, sacct -j and the backfill/time-limit note on the sbatch, sched_config, squeue, scancel and sacct pages. Removed: nothing removed.

Method: documentation only; no commands were run.
