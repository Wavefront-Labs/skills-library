---
id: computing-software.software-engineering.hpc-parallel-computing.slurm-requeue-signals
name: slurm-requeue-signals
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, slurm-signal, requeue-job, preemption, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Time limit handling"
sources: ["https://slurm.schedmd.com/sbatch.html", "https://slurm.schedmd.com/scontrol.html", "https://slurm.schedmd.com/preempt.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requeue and signal handling

Goal: checkpoint before time limit.
- `#SBATCH --signal=B:USR1@300 --requeue`: `B:` sends the signal to the batch shell only (by default job steps get it, not the batch shell), 300 seconds before the end time; trap `USR1` in the script to checkpoint and resubmit.
- Preemption can requeue jobs (`PreemptMode=REQUEUE`; see the preemption guide), so checkpoint regularly on preemptible partitions.
- Use `scontrol requeue`.
Verify: job restarts and continues from checkpoint.

## Checked

2026-11-03. Confirmed against the official pages: --signal=[{R|B}:]sig@time semantics and --requeue (sbatch page), scontrol requeue, PreemptMode and requeue (preempt guide). Removed: nothing removed.

Method: documentation only; no commands were run.
