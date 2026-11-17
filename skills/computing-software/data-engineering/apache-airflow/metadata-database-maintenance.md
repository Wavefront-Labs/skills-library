---
id: computing-software.data-engineering.apache-airflow.metadata-database-maintenance
name: metadata-database-maintenance
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, metadata-database, airflow-db-clean, db-migrate, postgres, pgbouncer, database-backup, airflow-upgrade, archive-tables]
level: advanced
status: docs-checked
description: "Keep the Airflow metadata DB healthy: purge history with airflow db clean, back up before migrate, PgBouncer connection pooling, and spotting table bloat."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#clean
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html
  - https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata database maintenance

**Goal:** the metadata DB stays small and fast, survives upgrades, and never becomes the scheduler's bottleneck.

## Database choice
PostgreSQL 12+ or MySQL 8.0+ in production (the documented minimum for running several schedulers); SQLite only for local dev (no concurrency). Managed Postgres (RDS/Cloud SQL) with automated backups is the common choice. Put **PgBouncer** in front: every scheduler, worker, triggerer and API server process opens connections, and Celery/K8s workers multiply them.

## Purge history regularly
Tables like `task_instance`, `dag_run`, `log`, `xcom`, `job`, `rendered_task_instance_fields`, `task_instance_history` grow forever.
```bash
airflow db clean --clean-before-timestamp "<ISO_TIMESTAMP>" \
  --tables <COMMA_SEPARATED_TABLES> \
  --skip-archive --yes                        # omit --skip-archive to keep archive tables
airflow db clean ... --dry-run                # first, to see row counts
```
Run it as a scheduled maintenance DAG or a Kubernetes CronJob, in small date windows if tables are huge. Archive tables must be dropped explicitly (`airflow db drop-archived`).

Keep enough history for your audit and debugging needs; the UI's run history disappears with it.

## Upgrades
1. Back up the DB (snapshot).
2. `airflow db check-migrations` / read release notes for long migrations.
3. Stop schedulers/workers (or follow the Helm chart's migration job flow).
4. `airflow db migrate` (`db upgrade` in older 2.x).
5. Start components on the new version.
Large `task_instance` tables make migrations slow: clean **before** upgrading.

## Health signals
- Scheduler loop duration (`scheduler.scheduler_loop_duration`) and `dag_processing.total_parse_time` rising with high DB CPU -> DB is the bottleneck.
- Slow UI grid/graph for DAGs with long history -> row counts too high.
- Connection-limit errors from the database -> pool sizing/PgBouncer.
Find the largest tables with your database's own tooling.

## Rules
- Never write to the metadata DB from DAG code (forbidden in Airflow 3 anyway).
- Do not share the metadata DB with application data.

## Verify
- [ ] Maintenance job runs weekly and logs deleted row counts.
- [ ] Largest tables stay roughly flat over months.
- [ ] Restore-from-backup tested once.

## Checked

2026-10-28. Confirmed in the Airflow CLI reference, upgrading page and scheduler page: `airflow db clean` with `--clean-before-timestamp`, `--tables`, `--skip-archive`, `-y`, `--dry-run`; `airflow db drop-archived`, `check-migrations`, `migrate`; PgBouncer as the recommended proxy; PostgreSQL 12+ / MySQL 8.0+; metrics `scheduler.scheduler_loop_duration` and `dag_processing.total_parse_time`. Removed: the date-arithmetic example, a hard-coded table list, archive-table naming, VACUUM advice, the retention figure, the CPU percentage and the pg_stat SQL.
Method: documentation only; no commands were run.
