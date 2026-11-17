---
id: computing-software.data-engineering.dagster.run-coordinators
name: run-coordinators
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, run-coordinator, queued-run-coordinator, default-run-coordinator, run-queue, concurrency-pools]
level: advanced
status: docs-checked
description: "Choose between DefaultRunCoordinator and QueuedRunCoordinator in Dagster and understand run queue dequeue ordering with concurrency pools."
sources:
  - https://docs.dagster.io/deployment/execution/run-coordinators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run coordinators

A run submitted from the UI or CLI goes first to the run coordinator, which applies any limits or prioritization policies before sending it to the run launcher.

- `DefaultRunCoordinator`: calls launch_run on the instance's run launcher immediately in the same process, with no limits or prioritization. With it, clicking **Launch Run** launches the run from the daemon process; scheduled runs launch from the scheduler process. No configuration needed.
- `QueuedRunCoordinator`: sends runs to the daemon via a run queue; the daemon pulls runs and calls launch_run. Enables instance-level run concurrency limits and custom run prioritization rules.

## Gotcha
When runs queue because a concurrency pool is at capacity, Dagster+ does not guarantee strict FIFO across all runs. Dequeue order follows internal prioritization logic, not strictly arrival time. If execution order matters, define explicit run prioritization rules with `QueuedRunCoordinator` (see the page Customizing run queue priority).

## Checked
2026-11-08. Confirmed against the Dagster docs page Run coordinators (raw markdown from the docs repo): both coordinator behaviours, configuration note, concurrency pool dequeue ordering caveat. Nothing removed.
Method: documentation only; no commands were run.
