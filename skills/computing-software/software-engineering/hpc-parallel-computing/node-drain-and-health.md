---
id: computing-software.software-engineering.hpc-parallel-computing.node-drain-and-health
name: node-drain-and-health
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, scontrol-update-node, drain-node, nodehealthcheck, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Operations"
sources: ["https://slurm.schedmd.com/scontrol.html", "https://slurm.schedmd.com/slurm.conf.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Draining nodes and health checks

Goal: handle bad nodes.
- `scontrol update NodeName=n001 State=drain Reason="disk"`, later `State=resume`.
- `HealthCheckProgram` runs periodically (`HealthCheckInterval`) and may verify a node; any drain must be done explicitly by the program, for example with the same `scontrol update` command.
- Investigate the slurmd log (`SlurmdLogFile` in slurm.conf).
Verify: drained node excluded from new jobs.

## Checked

2026-11-03. Confirmed against the official pages: scontrol update NodeName State=drain/resume Reason, HealthCheckProgram and HealthCheckInterval behaviour (slurm.conf page). Removed: the claim that NHC or HealthCheckProgram auto-drains nodes (the page says the program must drain explicitly) and the slurmd.log file name.

Method: documentation only; no commands were run.
