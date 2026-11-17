---
id: computing-software.data-engineering.prefect.state-types-and-transitions
name: state-types-and-transitions
category: computing-software
field: data-engineering
product: prefect
tags: [states, state-types, late, crashed, transitions]
level: practitioner
status: docs-checked
description: "Prefect state types versus names, terminal states, what Late, Failed and Crashed usually mean, and how return values map to states."
sources:
  - https://docs.prefect.io/v3/concepts/states
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read run states and diagnose stuck or failed runs.

Every run has a name (display) and a type (drives orchestration). Only runs have states; flows and tasks are templates.

| Type | Names |
|---|---|
| SCHEDULED | Scheduled, Late, AwaitingRetry, AwaitingConcurrencySlot, Resuming |
| PENDING | Pending, Submitting, InfrastructurePending |
| RUNNING | Running, Retrying |
| PAUSED | Paused, Suspended |
| CANCELLING | Cancelling |
| CANCELLED | Cancelled (terminal) |
| COMPLETED | Completed, Cached, RolledBack (terminal) |
| FAILED | Failed, TimedOut (terminal) |
| CRASHED | Crashed (terminal) |

Final categories: COMPLETED (returned successfully), FAILED (error such as raised exception), CRASHED (OS-level interruption such as keyboard interrupt or unexpected SIGTERM).

Normal path: Scheduled, Pending, Submitting, InfrastructurePending, Running, Completed.
- Scheduled to Late (default wait 15 seconds): no healthy worker, worker polling the wrong pool or queue, or concurrency limits reached.
- Running to Failed: code raised; check logs.
- Pending or Running to Crashed: infrastructure trouble such as OOM, evicted pods or timeouts; Pending to Crashed can mean missing code or broken imports.
- Retries: Failed, AwaitingRetry, Retrying.

Tasks returning any object end `Completed`, except returning a `Failed` state. `return_state=True` gives a State with `is_completed()`, `is_failed()` and `result()`.

## Checked
2026-11-08. Confirmed against the States concept page: name versus type, the full name, type and terminal table, the 15 second Late default, the transition explanations, final-state categories and task return value rules with return_state=True. Nothing removed.
Method: documentation only; no commands were run.
