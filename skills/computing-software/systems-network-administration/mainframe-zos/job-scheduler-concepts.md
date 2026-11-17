---
id: computing-software.systems-network-administration.mainframe-zos.job-scheduler-concepts
name: job-scheduler-concepts
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, tws, control-m, job-dependencies, batch-scheduler, automation, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Batch design"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Job scheduling and dependencies

Goal: design reliable batch.
- Schedulers (IBM Z Workload Scheduler, Control-M and equivalents) define calendars, predecessors and restart points.
- Make jobs restartable (checkpointing, GDG versions, idempotent steps).
- Keep run documentation and recovery steps per job.
Verify: a failed job restarts without manual data fixes.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
