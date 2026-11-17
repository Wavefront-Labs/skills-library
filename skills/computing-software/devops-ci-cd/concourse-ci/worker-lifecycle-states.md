---
id: computing-software.devops-ci-cd.concourse-ci.worker-lifecycle-states
name: worker-lifecycle-states
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [worker, lifecycle, landing, retiring, stalled, sigusr1, sigusr2]
level: practitioner
status: docs-checked
description: "Understand Concourse worker states (RUNNING, STALLED, LANDING, LANDED, RETIRING), the commands and signals that move a worker between them, and how the TSA reports them."
sources:
  - https://concourse-ci.org/docs/internals/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Concourse worker is always in one of five states.

- **RUNNING**: registered with the cluster and ready to run containers and store volumes.
- **STALLED**: it was registered but stopped advertising itself, usually from network problems or the worker stopping unexpectedly. If it cannot recover, remove it with `fly prune-worker`.
- **LANDING**: entered with the `concourse land-worker` command or by sending the worker process `SIGUSR1`. It drains assignments for temporary downtime. The ATC waits for builds on the worker for jobs that are uninterruptible to finish, then moves it to LANDED.
- **LANDED**: all uninterruptible jobs have finished. The worker receives no new containers or volumes until it registers as RUNNING again.
- **RETIRING**: entered with `concourse retire-worker` or `SIGUSR2`. The ATC waits for uninterruptible builds and then removes the worker permanently.

The worker sends these state changes through the TSA over SSH: `land-worker` initiates the move to LANDING and `retire-worker` the move to RETIRING. If draining is interrupted while retiring, the worker sends `delete-worker`, which removes it from the ATC. Landing is the right choice for a restart or short maintenance; retiring is for scaling down or replacing a machine permanently.

Two TSA commands support cleanup. `sweep-containers` and `sweep-volumes` return the handles of objects in the `DESTROYING` state for the worker to destroy, while `report-containers` and `report-volumes` send everything the worker holds so the ATC can drop destroyed entries and mark absent `CREATED` ones as missing.

## Checked

Checked 2026-11-09 against the raw docs source of the Internals page (read in full): states, signals, land and retire semantics and TSA commands all confirmed. The landing versus retiring advice restates the page's "temporary downtime" and "permanently" wording.

Method: docs-checked 2026-11-09 against concourse docs internals page (github.com/concourse/docs source); documentation only, no commands were run.
