---
id: computing-software.data-engineering.dagster.troubleshooting-concurrency
name: troubleshooting-concurrency
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, queued-runs, stale-slots, max-concurrent-runs, concurrency, troubleshooting]
level: advanced
status: docs-checked
description: "Debug Dagster runs stuck in QUEUED or skipping the queue: daemon, shared DAGSTER_HOME, max_concurrent_runs 0, and stale pool slots from cancelled runs."
sources:
  - https://docs.dagster.io/guides/operate/managing-concurrency/troubleshooting-concurrency
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting concurrency

## Runs skip QUEUED (OSS only)
Before 1.10.0 you may need to set the `run_queue` key in instance settings. Check **Deployment > Configuration**.

## Runs stay QUEUED
Dagster+: Hybrid agent is down (runs pause) or a Dagster+ outage.

OSS:
1. Daemon running? **Deployment > Daemons**, and **Run queue** should run. `dagster dev` starts it.
2. Daemon and webserver must use the same storage, same `dagster.yaml`, same `DAGSTER_HOME`.
3. Read daemon logs, which include skipped runs.
4. `concurrency.runs.max_concurrent_runs` of 0 can block the queue (check **Deployment > Configuration**).
5. Open **Runs** and the **Queued** and **In Progress** tabs; terminate blockers.

## Blocked by cancelled runs
Daemon logs say `Run <id> is blocked by global concurrency limits` with `pending_step_run_ids` listing a run in CANCELED or FAILURE. Cause: slots are not freed by default.

Fix: `run_monitoring` with `enabled: true` and `free_slots_after_run_end_seconds: 300`.

Immediate recovery: **Deployment > Concurrency** and release the slots, or CLI `dagster instance concurrency set <pool_name> <limit>`.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/operate/managing-concurrency/troubleshooting-concurrency

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
