---
id: computing-software.devops-ci-cd.deployment-strategies.migration-linting-with-squawk
name: migration-linting-with-squawk
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, migration-linting, squawk, database-migrations]
level: practitioner
status: docs-checked
description: "Lint PostgreSQL migrations in CI with squawk (or atlas lint) to catch lock-heavy, blocking or backward-incompatible DDL before it reaches production."
sources: ["https://squawkhq.com/docs/", "https://www.postgresql.org/docs/current/explicit-locking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration linting in CI (squawk)

Postgres DDL that looks harmless can take an `ACCESS EXCLUSIVE` lock and stall all traffic.
squawk lints SQL migration files for these patterns.

```bash
pip install squawk-cli       # or npm i -g squawk-cli
squawk migrations/20261018_add_index.sql
```
GitHub Actions on changed files:
```yaml
- run: |
    files=$(git diff --name-only origin/main...HEAD -- 'migrations/*.sql')
    [ -z "$files" ] || squawk $files
```
(For ORMs that generate SQL, emit the SQL first and lint that file.)

## What it catches (examples)
| Rule | Problem | Safe alternative |
|---|---|---|
| require-concurrent-index-creation | `CREATE INDEX` blocks writes | `CREATE INDEX CONCURRENTLY` (outside a transaction) |
| adding-field-with-default (old PG) / adding-required-field | table rewrite or failure | add nullable, backfill, then `SET NOT NULL` via `CHECK ... NOT VALID` + validate |
| constraint-missing-not-valid | FK/check validation scans table under lock | `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` |
| changing-column-type | rewrite + lock | new column + backfill + swap |
| renaming-column / renaming-table | breaks running app versions | expand/contract |
| prefer-robust-stmts | non-idempotent DDL | `IF NOT EXISTS` |
| ban-drop-column | breaks old app version | drop in a later release |

Configure in `.squawk.toml` (`excluded_rules`, `pg_version`, `assume_in_transaction = true` for
frameworks wrapping migrations in transactions).

Also set `lock_timeout` in migrations (`SET lock_timeout = '5s'`) so a blocked DDL fails fast instead of queueing traffic behind it.

## Verify
- [ ] A plain `CREATE INDEX` in a PR fails CI with the concurrency rule.

## Checked

2026-10-28. Confirmed against the squawk docs: install via `npm install -g squawk-cli` or `pip install squawk-cli`; rule names require-concurrent-index-creation, adding-field-with-default, adding-required-field, constraint-missing-not-valid, changing-column-type, renaming-column, renaming-table, prefer-robust-stmts and ban-drop-column; `.squawk.toml` with `excluded_rules`, `pg_version` and `assume_in_transaction`. PostgreSQL docs confirm ACCESS EXCLUSIVE locks, `CREATE INDEX CONCURRENTLY`, `NOT VALID` constraints and `lock_timeout`. Removed: the Django, Rails and Prisma command examples.

Method: documentation only; no commands were run.
