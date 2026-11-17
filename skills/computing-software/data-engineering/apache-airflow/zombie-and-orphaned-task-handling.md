---
id: computing-software.data-engineering.apache-airflow.zombie-and-orphaned-task-handling
name: zombie-and-orphaned-task-handling
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, zombie-task-detection, heartbeat-timeout, orphaned-tasks, task-adoption]
level: advanced
status: docs-checked
description: "Diagnose Airflow zombie (heartbeat timeout) and orphaned tasks: heartbeat settings, OOM-killed workers, executor adoption after scheduler restarts, and safe retries."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#task-instance-heartbeat-timeout
  - https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#scheduler
  - https://airflow.apache.org/docs/apache-airflow/stable/troubleshooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zombie / heartbeat-timeout and orphaned tasks

**Goal:** explain why a task was failed "without logs" and stop it recurring.

## Definitions
- **Zombie** (Airflow 3 calls it a *task instance heartbeat timeout*): the TI is `running` in the DB but its process stopped heartbeating. The scheduler fails it (and retries if retries remain). Threshold: `[scheduler] task_instance_heartbeat_timeout`, default 300 s.
- **Orphaned**: the TI is `queued`/`running` in the DB but no executor owns it, typically after a scheduler restart. The new scheduler tries to **adopt** it; otherwise it is reset. Check interval: `[scheduler] orphaned_tasks_check_interval`.

## Usual root causes
1. Worker pod/process **OOM-killed** or node evicted. Look at the pod events and the node's kernel log, not Airflow logs.
2. Metadata DB overloaded so heartbeats cannot be written.

## Actions
- Raise memory requests/limits for the task (per-task executor settings) or move it to bigger workers.
- Make tasks idempotent and give them `retries` so a heartbeat timeout retries cleanly.
- Set `execution_timeout` on long tasks so hangs fail fast instead of zombifying.
- Do not just raise the heartbeat timeout: it delays detection of real deaths.

## Find them
Scheduler log lines mentioning the heartbeat timeout, and task instances with no task log and a failure note.

## Verify
After fixing, no new heartbeat-timeout failures appear over a full run cycle and OOM events disappear from node logs.

## Checked

2026-10-28. Confirmed against: configuration reference ([scheduler] task_instance_heartbeat_timeout default 300, orphaned_tasks_check_interval). Removed (not confirmable in the fetched pages): Airflow 2 option name, adoption support list, Celery visibility_timeout, pod_override, metric names, log line text, exit code.

Method: documentation only; no commands were run.
