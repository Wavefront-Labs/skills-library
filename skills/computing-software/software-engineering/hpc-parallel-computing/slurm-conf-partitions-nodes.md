---
id: computing-software.software-engineering.hpc-parallel-computing.slurm-conf-partitions-nodes
name: slurm-conf-partitions-nodes
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, slurm-conf-file, nodename, partitionname, slurm-conf, slurmctld, slurmd, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Cluster config"
sources: ["https://slurm.schedmd.com/slurm.conf.html", "https://slurm.schedmd.com/scontrol.html", "https://slurm.schedmd.com/slurmd.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slurm.conf, nodes and partitions

Goal: configure a cluster.
- `NodeName=n[001-064] CPUs=64 RealMemory=256000 Gres=gpu:4 State=UNKNOWN`; `PartitionName=compute Nodes=n[001-064] MaxTime=48:00:00 State=UP`.
- Daemons: `slurmctld`, `slurmd`, `slurmdbd`; reload with `scontrol reconfigure`.
- Validate hardware with `slurmd -C`.
Verify: `sinfo` shows nodes idle.

## Checked

2026-11-03. Confirmed against the official pages: NodeName/PartitionName parameters CPUs, RealMemory, Gres, State, Nodes, MaxTime; the daemons; scontrol reconfigure; slurmd -C. Removed: nothing removed.

Method: documentation only; no commands were run.
