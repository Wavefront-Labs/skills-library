---
id: computing-software.devops-ci-cd.deployment-strategies.testing-migrations-against-production-like-data
name: testing-migrations-against-production-like-data
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, migration-testing, database-migrations, online-schema-change]
level: advanced
status: docs-checked
description: "Rehearse database migrations on production-sized, anonymised data before release: timing, lock duration, replication lag, rollback scripts and old-app compatibility."
sources: ["https://www.postgresql.org/docs/current/view-pg-locks.html", "https://www.postgresql.org/docs/current/monitoring-stats.html", "https://www.postgresql.org/docs/current/runtime-config-client.html", "https://www.postgresql.org/docs/current/sql-altertable.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing migrations against production-like data

A migration that is instant on a fixture DB can run far longer and hold locks on a large production table.

## Rehearsal environment
- Restore a recent **anonymised** snapshot (or a copy-on-write branch) of production with the same
  Postgres/MySQL version and similar instance size.
- Include replicas if you rely on them; DDL replication lag matters.

## What to measure
```sql
SET lock_timeout = '5s';
BEGIN; -- or not, per your framework
ALTER TABLE orders ADD COLUMN channel text;
COMMIT;
```
- Wall time of each migration step.
- Locks held: from another session during the run, query `pg_locks` joined to `pg_stat_activity` on `pid` for the migrated table.
- Replica lag (`pg_stat_replication.replay_lag`), disk growth (index builds need space).
- Behaviour with concurrent load: replay traffic or run a load script against the app during the migration.

## Compatibility checks
- Run the **previous** app version's test suite against the migrated schema (old code + new schema
  must work during rolling deploys).
- Run the rollback/down migration if you rely on it, and measure it too.

## Automate
Nightly or pre-release job: restore snapshot, apply pending migrations, record durations, fail if a
step exceeds a budget (e.g. 30 s for any locking step) and post results to the release ticket.
A migration linter for your framework helps enforce safe patterns.

## Verify
- [ ] Release checklist links a rehearsal report with timings for every migration in the release.

## Checked

2026-10-28. Confirmed against the PostgreSQL docs: `pg_locks` (current locks), `pg_stat_replication.replay_lag`, `lock_timeout`, and `ALTER TABLE ... ADD COLUMN`. Removed: the specific timing and size figures in the opening line, the `regclass` query form, the k6 reference, and the strong_migrations and django-pg-zero-downtime-migrations tool claims (their sources could not be read).

Method: documentation only; no commands were run.
