---
id: computing-software.data-engineering.apache-airflow.airflow-3-dag-migration
name: airflow-3-dag-migration
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-3-migration, airflow-3-breaking-changes, ruff-air-rules, execution-date-removed, airflow-sdk-imports, catchup-default, subdag-removed, sla-removed, subdag-removal, standard-provider]
level: advanced
status: verified
description: "Migrate DAGs to Airflow 3: ruff AIR30x rules with --fix, removed context keys like execution_date, airflow.sdk imports, new schedule/catchup defaults, SubDAG/SLA removal."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html
  - https://docs.astral.sh/ruff/rules/#airflow-air
  - https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Migrating DAG code to Airflow 3

**Goal:** DAG files that parse and behave the same on Airflow 3, found mechanically where possible.

## 1. Upgrade to latest 2.x first
Official guide: upgrade to Airflow 2.7 or later, ideally the latest 2.x release first, fix deprecation warnings, then move to 3.

## 2. Let ruff find the breakage
```bash
pip install "ruff>=0.13.1"   # version the official guide names
ruff check dags/ plugins/ --preview --select AIR301,AIR302          # removed / moved-to-provider (must fix)
ruff check dags/ plugins/ --preview --select AIR311,AIR312          # recommended updates
ruff check dags/ plugins/ --preview --select AIR3 --fix              # auto-fix what is safe
```
AIR301: removed in 3.0; AIR302: moved to a provider package (install it, change import); AIR311/312: still works but should change.

## 3. Common manual changes
| Airflow 2 | Airflow 3 |
|---|---|
| `execution_date`, `prev_execution_date`, `next_execution_date` (and the other legacy date keys; ruff AIR301 flags them) in context/templates | `logical_date`, `data_interval_start/end` (confirm replacements for the `prev_*` keys in the upgrade guide) |
| `schedule_interval=` / `timetable=` | `schedule=` |
| `from airflow.decorators import dag, task`, `from airflow.models import DAG, BaseOperator` | `from airflow.sdk import dag, task, DAG, BaseOperator, Asset, Variable` |
| `Dataset` | `Asset` |
| BashOperator/PythonOperator in core | `apache-airflow-providers-standard` package |
| SubDAGs | Task groups / assets |
| `sla=` and `sla_miss_callback` | Removed; Deadline Alerts replace them |
| `catchup` default True | Default False (`[scheduler] catchup_by_default`) |
| Bare cron string gives data-interval timetable | `create_cron_data_intervals` now False: `CronTriggerTimetable` (no data interval). Set it True before upgrading to keep the old behaviour |
| `/api/v1` REST | FastAPI-based `/api/v2` |

## 4. Behavioural checks
- DAGs computing "yesterday" from `data_interval_start` under a cron schedule: verify the new default timetable or set `CronDataIntervalTimetable` explicitly.
- Code that read/wrote the metadata DB fails: the guide says task code can no longer import Airflow DB sessions or models directly.
- Custom operators/plugins using removed internals: run ruff AIR301 and the Airflow 3 import test to find them.

## 5. Test
Run the DAG integrity tests and `dag.test()` for representative DAGs in an Airflow 3 image; compare produced data intervals and outputs against 2.x runs for the same dates.

## Verify
- [ ] `ruff check --select AIR301,AIR302 --preview` returns no findings.
- [ ] All DAGs import in the Airflow 3 image (DagBag test green).
- [ ] Sample DAG runs on 3.x process the same windows as on 2.x.
