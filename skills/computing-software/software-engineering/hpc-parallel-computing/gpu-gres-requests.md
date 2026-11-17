---
id: computing-software.software-engineering.hpc-parallel-computing.gpu-gres-requests
name: gpu-gres-requests
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, gres-gpu, sbatch-gpus, cuda-visible-devices, slurm-gres, slurm-memory, slurm-cpus-per-task, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Accelerators in Slurm"
sources: ["https://slurm.schedmd.com/gres.html", "https://slurm.schedmd.com/sbatch.html", "https://slurm.schedmd.com/sinfo.html", "https://slurm.schedmd.com/cgroup.conf.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPUs and GRES

Goal: request GPUs.
- `--gres=gpu:a100:2` or `--gpus-per-node=2`; Slurm sets `CUDA_VISIBLE_DEVICES`.
- Use `--gpu-bind` for mapping; `ConstrainDevices` in cgroup.conf restricts device access.
- GPU type names are site-specific (`sinfo -o "%N %G"`).
Verify: `echo $CUDA_VISIBLE_DEVICES` inside the job lists only the allocated GPUs.

## Checked

2026-11-03. Confirmed against the official pages: --gres=gpu:type:count, --gpus-per-node, --gpu-bind, CUDA_VISIBLE_DEVICES, ConstrainDevices, sinfo %N/%G. Removed: the claim that nvidia-smi inside a job shows only allocated GPUs (replaced by the documented CUDA_VISIBLE_DEVICES behaviour).

Method: documentation only; no commands were run.
