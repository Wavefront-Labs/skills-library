---
id: computing-software.database-administration.sql.migration-testing-in-ci
name: migration-testing-in-ci
category: computing-software
field: database-administration
product: sql
tags: [sql, migration-testing-in-ci]
level: practitioner
status: draft
description: "Verify migrations apply cleanly on a fresh database and on a production-shaped copy."
sources: ["https://www.postgresql.org/docs/current/", "https://www.sqlite.org/lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing migrations in CI

- CI job: start a throwaway database (container), apply all migrations from empty, run a schema diff against the expected state, then apply the newest migration on a dump of the previous schema.
- Check idempotence and down-migrations where used.
- Measure lock time with a large synthetic table.
- Tools: Flyway, Liquibase, sqitch, Alembic, `sqlite3` with `PRAGMA user_version`.
- Self-check: CI fails on a deliberately broken migration.
