---
id: computing-software.data-engineering.apache-airflow.db-migrate-and-minor-upgrades
name: db-migrate-and-minor-upgrades
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-db-migrate, airflow-upgrade, metadata-database, alembic, db-downgrade, helm-chart, upgrade-runbook]
level: practitioner
status: docs-checked
description: "Upgrade Airflow minor/patch versions safely: backup, airflow db migrate (offline SQL option), Helm migration job, component order, downgrade path and post-checks."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading.html
  - https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#migrate
  - https://airflow.apache.org/docs/helm-chart/stable/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# airflow db migrate and minor upgrades

**Goal:** move from e.g. 2.9 -> 2.10 or 3.0 -> 3.1 with a predictable outage window and a way back.

## Runbook
1. **Read release notes** for every version in between (significant changes, removed configs, provider minimums).
2. **Test** the new image in staging against a copy of the prod metadata DB: run migrations, DagBag import, a few DAGs.
3. **Clean the DB first** (makes migrations faster): `airflow db clean --clean-before-timestamp '<ISO_TIMESTAMP>' --skip-archive --yes` (or archive).
4. **Backup** the metadata DB (snapshot/pg_dump).
5. **Pause scheduling**: scale scheduler/dag-processor/triggerer to 0 (or pause DAGs) and let running tasks finish or accept they will be retried.
6. **Migrate**:
```bash
airflow db migrate                       # upgrades schema to the installed version
airflow db migrate --show-sql-only       # print SQL for DBA review (offline)
airflow db migrate -n 2.10.0             # to a specific version
```
   Helm chart: the `migrateDatabaseJob` runs the migration on install/upgrade (see its `useHelmHooks` value); ensure the job completes before rolling out components.
7. **Roll out** all components on the new image (scheduler, api-server/webserver, workers, triggerer, dag-processor).
8. **Post-checks**: `airflow db check`, `airflow dags list-import-errors`, UI loads, a canary DAG run succeeds, `airflow providers list` versions as expected.

## Downgrade
```bash
airflow db downgrade --to-version 2.9.3 --show-sql-only    # review
airflow db downgrade --to-version 2.9.3 -y
```
Review the SQL first, then deploy the old image. Restoring the backup is simpler if the window is short and no new runs matter.

## Gotchas
- Use `airflow db migrate` for schema upgrades.
- Long migrations on large `task_instance`/`xcom`/`log` tables: clean first, and run outside peak; some migrations add columns with backfill.
- MySQL: the global variable `explicit_defaults_for_timestamp` must be on (1).
- Provider packages installed separately may require a newer Airflow core; use the constraints file of the target version.

## Verify
- [ ] `airflow db check-migrations` returns success on every component.
- [ ] Canary DAG and one heavy DAG succeed after upgrade; no new import errors.

## Checked

2026-10-28. Confirmed in the Airflow CLI reference, upgrading page and Helm chart page: `airflow db migrate` with `--show-sql-only` and `-n`/`--to-version`, `airflow db downgrade --to-version`, `db check`, `db check-migrations`, `db clean --clean-before-timestamp --skip-archive -y`, `airflow dags list-import-errors`, `migrateDatabaseJob`, and the MySQL `explicit_defaults_for_timestamp` requirement. Removed: the migration job's kubectl name, the db upgrade/init rename note, the mixed-version and downgrade-direction claims, and the collation note.
Method: documentation only; no commands were run.
