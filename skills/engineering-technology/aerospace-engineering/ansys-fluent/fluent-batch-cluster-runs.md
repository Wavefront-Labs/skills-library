---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-batch-cluster-runs
name: fluent-batch-cluster-runs
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-hpc, fluent-batch, hpc, slurm, batch-submission, journal-file, restart]
level: practitioner
status: draft
description: "Submit Fluent batch jobs on an HPC scheduler with a journal file, a host file and licence settings, and monitor and restart them reliably."
sources:
  - "Ansys Fluent user guide (parallel processing and batch options)"
  - "Scheduler (Slurm) documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent batch runs on a cluster

**Goal:** unattended, restartable runs.

## Job script pattern (Slurm example)
```bash
#!/bin/bash
#SBATCH --job-name=fluent_run
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --time=12:00:00
module load ansys   # site-specific
scontrol show hostnames $SLURM_JOB_NODELIST > hosts.txt
fluent 3ddp -g -t$SLURM_NTASKS -cnf=hosts.txt -mpi=openmpi -i run.jou > run.log 2>&1
```
MPI flag and scheduler integration options (for example `-scheduler=slurm`) depend on the site's installation; use the site documentation.

## Journal
```
/file/read-case-data case.cas.h5
/solve/iterate 2000
/file/write-case-data out.cas.h5
/exit yes
```
Add autosave: `/file/auto-save/data-frequency 200` and `/file/auto-save/root-name auto`.

## Practice
- Write results regularly; restart from the last autosave if the job is killed.
- Check the licence availability before submit; failed checkouts end jobs silently in the log.
- Check log for the line count of "iter" progress and for divergence messages.

## Gotchas
- Wall-clock limit kills the job: save before the limit using a time-based exit script.
- Mixed MPI libraries on different nodes cause startup hangs.

## Verify
- [ ] Log ends with a clean exit and the output case and data files exist.
