---
id: computing-software.data-engineering.prefect.database-maintenance
name: database-maintenance
category: computing-software
field: data-engineering
product: prefect
tags: [vacuum, retention, postgres, autovacuum, bloat]
level: sme
status: docs-checked
description: "Maintain the Prefect server PostgreSQL database: the db vacuum service settings, event retention, autovacuum tuning, bloat thresholds and remediation."
sources:
  - https://docs.prefect.io/v3/advanced/database-maintenance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a self-hosted Postgres database small and healthy.

Vacuum service settings (defaults):
- `PREFECT_SERVER_SERVICES_DB_VACUUM_ENABLED`: `events` (options `events`, `flow_runs`, `orphans`)
- `..._LOOP_SECONDS`: 3600
- `..._ORPHAN_CLEANUP_LOOP_SECONDS`: 86400
- `..._RETENTION_PERIOD`: 7776000 (90 days; must exceed 1 hour)
- `..._BATCH_SIZE`: 200
- `..._EVENT_RETENTION_OVERRIDES`: `{"prefect.flow-run.heartbeat": 604800}`

`flow_runs` is off by default and permanently deletes data; back up first. `orphans` is enabled automatically with `flow_runs` and runs daily. Event vacuum needs the event persister (`PREFECT_SERVER_SERVICES_EVENT_PERSISTER_ENABLED`, on by default).

Event retention: `PREFECT_SERVER_EVENTS_RETENTION_PERIOD`, default 7 days. Suggested: under 100 runs/day keep 7 days; 100 to 1000 runs/day 3 to 5 days; over 1000 runs/day 1 to 2 days.

Bloat: under 20% normal; 20 to 50% monitor; over 50% manual VACUUM; over 100% urgent. Red flags: disk over 80%, connections near the limit, no autovacuum in 24+ hours.

Autovacuum per table: `events` scale factor 0.05 (default 0.2), threshold 1000, analyze scale 0.02; `flow_run_state` vacuum 0.1, analyze 0.05; `flow_run` vacuum 0.1, threshold 500.

Remediation: manual `VACUUM ANALYZE` on high-bloat tables; prefer pg_repack over `VACUUM FULL`, which takes an exclusive lock and can run for hours.

Custom retention flows that delete with SQL bypass application cascades and can orphan logs and artifacts; afterwards enable `orphans`. Preview with a SELECT first.

## Checked

2026-11-09. Confirmed: Database maintenance page (docs.prefect.io/v3/advanced/database-maintenance): vacuum service settings table and defaults, flow_runs off by default, orphans, event persister dependency, retention table, bloat thresholds, red flags, autovacuum values, VACUUM FULL versus pg_repack, SELECT-first advice. Nothing removed.

Method: documentation only; no commands were run.
