---
id: computing-software.software-engineering.hpc-parallel-computing.dask-on-slurm
name: dask-on-slurm
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, dask-jobqueue, slurmcluster, dask-workers, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Python parallelism"
sources: ["https://jobqueue.dask.org/en/latest/generated/dask_jobqueue.SLURMCluster.html", "https://jobqueue.dask.org/en/latest/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dask on Slurm

Goal: scale Python analysis.
- `SLURMCluster(cores=16, memory='64GB', walltime='01:00:00')`, `cluster.scale(jobs=10)`, `Client(cluster)`.
Verify: workers appear in `squeue` and tasks complete.

## Checked

2026-11-03. Confirmed against the official pages: SLURMCluster cores, memory and walltime parameters, cluster.scale(jobs=10) and Client(cluster) (dask-jobqueue docs). Removed: the >100 ms task-size rule, dashboard and scratch advice.

Method: documentation only; no commands were run.
