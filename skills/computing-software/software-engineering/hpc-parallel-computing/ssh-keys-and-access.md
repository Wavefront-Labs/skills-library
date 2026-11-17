---
id: computing-software.software-engineering.hpc-parallel-computing.ssh-keys-and-access
name: ssh-keys-and-access
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, ssh-config, login-node-etiquette, proxyjump, ssh-hpc, quota, fair-use, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Using clusters"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSH access and etiquette

Goal: work well on shared systems.
- Keys not passwords; `~/.ssh/config` with `ProxyJump`; use `tmux` for sessions.
- No heavy compute on login nodes.
- Check `quota`/`lfs quota` and clean scratch.
Verify: jobs run via the scheduler only.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
