---
id: computing-software.data-engineering.apache-airflow.scheduler-and-concurrency-tuning
name: scheduler-and-concurrency-tuning
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-parallelism, scheduler-tuning, max-active-tasks-per-dag, worker-concurrency, dag-processor, min-file-process-interval, multiple-schedulers, queued-tasks]
level: advanced
status: docs-checked
description: "Scale Airflow: the concurrency knobs from parallelism down to pools and worker_concurrency, why tasks sit queued, DAG parsing settings, and running multiple schedulers."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html
  - https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html
  - https://airflow.apache.org/docs/apache-airflow/stable/faq.html#why-is-task-not-getting-scheduled
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduler and concurrency tuning

**Goal:** tasks start promptly when capacity exists, and limits protect downstream systems rather than starving Airflow itself.

## The limit stack (a task runs only if every level has room)
| Level | Setting | Default |
|---|---|---|
| Installation | `[core] parallelism` (per scheduler: max running+queued task instances) | 32 |
| DAG | `max_active_tasks` (DAG arg) / `[core] max_active_tasks_per_dag` | see configuration reference |
| DAG runs | `max_active_runs` / `[core] max_active_runs_per_dag` | 16 |
| Task | `max_active_tis_per_dag` (task parameter) | |
| Pool | `pool` (default_pool has 128 slots) | |
| Executor | Celery worker concurrency x workers; K8s cluster capacity | |
Tasks "stuck in scheduled/queued" usually hit one of these: check pools page (Running/Queued/Open slots), `parallelism`, and worker capacity first.

## Typical production starting point
```ini
[core]
parallelism = 256                  # >= sum of worker slots
max_active_tasks_per_dag = 32
[scheduler]
max_tis_per_query = 64             # tasks examined per loop (default 16)
[celery]
worker_concurrency = 16            # per worker; size to worker CPU/memory and task type
```
Use **pools** to cap load on shared systems (e.g. pool `warehouse` 20 slots), not `parallelism`.

## DAG parsing
- `[dag_processor] min_file_process_interval` (default 30 s): raise it for many static DAG files.
- `[dag_processor] refresh_interval`: how often new files are discovered (it replaces the deprecated `[scheduler] dag_dir_list_interval`).
- `parsing_processes` = CPU cores available to the processor.
- Biggest win: fast-parsing DAG files (no top-level I/O). Check `airflow dags report` for per-file parse time.
- Airflow 3 runs the DAG processor as a separate component (`airflow dag-processor`); scale it independently.

## Multiple schedulers
Airflow 2.0+ supports active-active schedulers (row-level locking; requires Postgres 12+/MySQL 8+). Run 2 for HA; add more only when scheduler loop time is the measured bottleneck.

## Key metrics
`scheduler.tasks.starving`, `scheduler.tasks.executable`, `executor.open_slots`, `executor.queued_tasks`, `pool.open_slots`, `scheduler.scheduler_loop_duration`, `dag_processing.total_parse_time`.

## Verify
- [ ] Under a burst, queued tasks drain at roughly worker capacity, with no pool or parallelism ceiling hit unexpectedly.
- [ ] `total_parse_time` well under `min_file_process_interval`.
- [ ] Killing one scheduler does not stop scheduling.

## Checked

2026-10-28. Confirmed in the Airflow configuration reference, scheduler page and metrics page: `[core] parallelism` default 32, `max_active_runs_per_dag` default 16, default pool 128 slots, `[scheduler] max_tis_per_query` default 16, `[dag_processor] min_file_process_interval` default 30, `refresh_interval`, `dag_dir_list_interval` deprecated, PostgreSQL 12+ / MySQL 8.0+ for multiple schedulers, `airflow dags report`, the listed scheduler/executor metrics. Removed: unconfirmed `max_active_tis_per_dagrun`, `pool_slots`, `worker_concurrency` default and `max_active_tasks_per_dag` default, and the 120-300 s advice.
Method: documentation only; no commands were run.
