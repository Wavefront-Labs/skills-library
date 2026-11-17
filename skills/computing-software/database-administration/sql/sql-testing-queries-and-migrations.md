---
id: computing-software.database-administration.sql.sql-testing-queries-and-migrations
name: sql-testing-queries-and-migrations
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-testing, pgtap, test-data, migration-testing, explain-regression]
level: advanced
status: draft
description: "Test SQL: fixtures, pgTAP or dbt tests, migration checks and plan regressions in CI."
sources: ["https://www.postgresql.org/docs/current/", "https://www.sqlite.org/docs.html", "https://www.iso.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing SQL

- Run tests against the same engine and major version as production in a throwaway database (Docker, Testcontainers); SQLite stand-ins hide dialect differences.
- Unit style: pgTAP (`SELECT results_eq(...)`, `has_column`, `throws_ok`) for PostgreSQL; tSQLt for SQL Server; utPLSQL for Oracle; dbt tests (`unique`, `not_null`, `relationships`, custom) for warehouse models.
- Build minimal fixtures that include edge cases: NULLs, duplicates, ties, empty groups, time-zone boundaries, large ids.
- Migrations: apply from an empty database and from the previous release schema, assert schema diff (`pg_dump -s`, `migra`, `atlas`), and time them against a production-sized copy; check lock behaviour.
- Guard performance: assert that a key query's plan uses the expected index (`EXPLAIN (FORMAT JSON)`) or stays under a row/time budget on seeded data.
- Make tests idempotent and run each in a rolled-back transaction where possible.
