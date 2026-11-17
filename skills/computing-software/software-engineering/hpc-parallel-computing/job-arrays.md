---
id: computing-software.software-engineering.hpc-parallel-computing.job-arrays
name: job-arrays
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, sbatch-array, slurm-array-task-id, array-throttle, slurm-array, slurm-dependency, job-chains, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Many similar jobs"
sources: ["https://slurm.schedmd.com/sbatch.html", "https://slurm.schedmd.com/job_array.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job arrays

Goal: run parameter sweeps.
- `#SBATCH --array=0-99%10` runs 100 tasks, 10 at a time (the `%` separator limits simultaneously running tasks); `$SLURM_ARRAY_TASK_ID` selects input.
- Output pattern `%A_%a.out`: `%A` is the array job ID and `%a` the task index.
- A job array submits many similar jobs with one `sbatch` call.
Verify: all array tasks complete and outputs exist.

## Checked

2026-11-03. Confirmed against the official pages: --array syntax, the % throttle, SLURM_ARRAY_TASK_ID and the %A/%a filename patterns (job_array and sbatch pages). Removed: the claim that arrays reduce scheduler load (not stated on the pages read).

Method: documentation only; no commands were run.
