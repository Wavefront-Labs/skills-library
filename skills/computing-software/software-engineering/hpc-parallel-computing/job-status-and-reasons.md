---
id: computing-software.software-engineering.hpc-parallel-computing.job-status-and-reasons
name: job-status-and-reasons
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, squeue-reason, scontrol-show-job, sprio, squeue, sacct, scontrol, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Why isn't my job running"
sources: ["https://slurm.schedmd.com/squeue.html", "https://slurm.schedmd.com/scontrol.html", "https://slurm.schedmd.com/sprio.html", "https://slurm.schedmd.com/sinfo.html", "https://slurm.schedmd.com/sbatch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job state and pending reasons

Goal: diagnose pending jobs.
- `squeue -j id -o "%i %T %r"` prints job ID, state and reason; reasons include Resources, Priority and ReqNodeNotAvail, plus the `QOSMax*Limit` and `AssocGrp*Limit` families (see JOB REASON CODES on the squeue page).
- `scontrol show job id`, `sprio -j id`, `sinfo -R` for down nodes.
- `sbatch --test-only` validates the script and estimates start time without submitting.
Verify: you can state why a job waits.

## Checked

2026-11-03. Confirmed against the official pages: squeue %i/%T/%r and reason codes, scontrol show job, sprio -j, sinfo -R, sbatch --test-only. Removed: the specific reason names QOSMaxJobsPerUserLimit and AssocGrpCPUMinutesLimit (the page lists only the QOSMax*Limit and AssocGrp*Limit families).

Method: documentation only; no commands were run.
