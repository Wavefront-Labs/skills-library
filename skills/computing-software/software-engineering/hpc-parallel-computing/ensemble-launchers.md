---
id: computing-software.software-engineering.hpc-parallel-computing.ensemble-launchers
name: ensemble-launchers
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, gnu-parallel, hyperqueue, launcher, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Many small tasks"
sources: ["https://slurm.schedmd.com/srun.html", "https://slurm.schedmd.com/high_throughput.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ensemble launchers

Goal: avoid flooding the scheduler.
- `srun --multi-prog` runs different programs per task from a config file.
- Prefer one allocation that runs many steps over thousands of tiny jobs; Slurm's high-throughput guide covers tuning for many short jobs.
- Track completed tasks for restarts.
Verify: all tasks complete in one allocation.

## Checked

2026-11-03. Confirmed against the official pages: srun --multi-prog (srun page); the existence of the High Throughput Computing guide. Removed: GNU Parallel and HyperQueue (no pages read).

Method: documentation only; no commands were run.
