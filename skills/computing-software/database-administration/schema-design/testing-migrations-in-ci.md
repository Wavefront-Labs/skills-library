---
id: computing-software.database-administration.schema-design.testing-migrations-in-ci
name: testing-migrations-in-ci
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, migration-testing, ci-cd, schema-migrations, testcontainers, database-devops]
level: practitioner
status: draft
description: "Test schema migrations in CI/CD: apply from scratch and from a production-like snapshot, check reversibility, lock and duration risks, and lint dangerous DDL before merge."
sources:
  - https://testcontainers.com/modules/postgresql/
  - https://squawkhq.com/docs/
  - https://atlasgo.io/versioned/lint
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing migrations in CI/CD

## Pipeline stages
1. **Lint** the migration SQL for dangerous operations:
   - PostgreSQL: `squawk` flags `ADD COLUMN ... DEFAULT volatile`, `CREATE INDEX` without `CONCURRENTLY`, `ALTER COLUMN TYPE`, adding NOT NULL / FK without `NOT VALID`, missing `lock_timeout`.
   - MySQL: check for operations not supporting `ALGORITHM=INSTANT/INPLACE`; route big tables to gh-ost/pt-osc.
   - Generic: Atlas `atlas migrate lint`, Liquibase/Flyway policy checks.
2. **Apply from empty**: spin up the exact engine version (Testcontainers, docker-compose service) and run all migrations; schema must match the expected dump.
3. **Apply to a production-like snapshot**: restore a masked recent backup (or a subset with realistic sizes) and run the new migrations; record duration and locks.
4. **Reverse** (if you support down migrations): up → down → up must succeed and leave an identical schema.
5. **Run application tests** against the migrated schema, including the previous application version (N-1) to prove backward compatibility for rolling deploys.

## Example (GitHub Actions + PostgreSQL)
```yaml
services:
  postgres:
    image: postgres:16
    env: { POSTGRES_PASSWORD: ci }
    ports: ["5432:5432"]
steps:
  - uses: actions/checkout@v4
  - run: npx squawk-cli migrations/*.sql
  - run: flyway -url=jdbc:postgresql://localhost:5432/postgres -user=postgres -password=ci migrate
  - run: pg_dump -s -h localhost -U postgres postgres | grep -v '^--' > schema.actual.sql && diff -u schema.expected.sql schema.actual.sql
```

## Measuring lock risk
In the snapshot test, run with `SET lock_timeout = '2s'` and a concurrent synthetic workload; migrations that need long ACCESS EXCLUSIVE locks fail visibly in CI instead of in production. Log `pg_locks` during the run.

## Data migrations
Test backfills for correctness (row counts, checksums) and idempotency (running twice is harmless) on the snapshot.

## Gotchas
- CI on a different engine (SQLite instead of PostgreSQL) hides real failures; use the same major version.
- Seed data and extensions must match production (`CREATE EXTENSION` versions).

## Verify
A deliberately dangerous migration (non-concurrent index on a big table) fails the pipeline; migration duration on the snapshot is reported in the PR.
