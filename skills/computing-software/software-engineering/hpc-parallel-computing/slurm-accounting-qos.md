---
id: computing-software.software-engineering.hpc-parallel-computing.slurm-accounting-qos
name: slurm-accounting-qos
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, sacctmgr, slurm-qos, fairshare, hpc, parallel-programming, supercomputing]
level: practitioner
status: docs-checked
description: "Policy"
sources: ["https://slurm.schedmd.com/sacctmgr.html", "https://slurm.schedmd.com/qos.html", "https://slurm.schedmd.com/accounting.html", "https://slurm.schedmd.com/priority_multifactor.html", "https://slurm.schedmd.com/sshare.html", "https://slurm.schedmd.com/sprio.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accounting, QOS and fair share

Goal: enforce usage policy.
- `sacctmgr add account proj1`, `add user`, `modify qos` limits (`GrpTRES`, `MaxWall`, `MaxJobsPerUser`).
- Fair share via `PriorityType=priority/multifactor`; see `sshare` and `sprio`.
- Accounting needs slurmdbd with a database.
Verify: `sacctmgr show assoc` matches policy.

## Checked

2026-11-03. Confirmed against the official pages: sacctmgr add/modify/show, QOS limits GrpTRES, MaxWall and MaxJobsPerUser (documented as MaxJobsPU), priority/multifactor, sshare, sprio, slurmdbd with MySQL/MariaDB. Removed: nothing removed.

Method: documentation only; no commands were run.
