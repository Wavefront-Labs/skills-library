---
id: computing-software.database-administration.schema-design.declarative-and-reversible-schema-tools
name: declarative-and-reversible-schema-tools
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, atlas-schema, sqitch, pgroll, declarative-migrations, schema-migrations]
level: practitioner
status: draft
description: "Use declarative and reversible schema tools: Atlas (desired-state diffs, linting), Sqitch (deploy/revert/verify changes) and pgroll (zero-downtime expand/contract)."
sources:
  - https://atlasgo.io/getting-started
  - https://sqitch.org/docs/manual/sqitchtutorial/
  - https://github.com/xataio/pgroll
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Declarative and reversible schema tools (Atlas / Sqitch / pgroll)

## Atlas: declarative desired state
Define the target schema (HCL, SQL, or ORM models); Atlas computes the diff.
```bash
atlas schema inspect -u "postgres://app@db/app?sslmode=disable" > schema.hcl
atlas schema apply -u "$DB_URL" --to file://schema.sql --dev-url "docker://postgres/16/dev" --dry-run
# versioned workflow: generate migration files from desired state
atlas migrate diff add_status --dir file://migrations --to file://schema.sql --dev-url "docker://postgres/16/dev"
atlas migrate lint --dir file://migrations --dev-url "docker://postgres/16/dev" --latest 1
atlas migrate apply --dir file://migrations -u "$DB_URL"
```
The dev database (throwaway container) normalises and validates SQL. Lint detects destructive changes, table locks, backward-incompatible changes. Review planned SQL: renames still appear as drop+add unless declared.

## Sqitch: explicit changes with deploy/revert/verify
No ORM, plain SQL scripts per change, ordered by declared dependencies (not numbers):
```bash
sqitch init app --engine pg
sqitch add orders_status --requires orders -n "Add orders.status"
# edits: deploy/orders_status.sql, revert/orders_status.sql, verify/orders_status.sql
sqitch deploy db:pg://app@db/app
sqitch verify db:pg://app@db/app
sqitch revert --to @HEAD^ db:pg://app@db/app
sqitch rework orders_view   # new version of a function/view while keeping history
```
Verify scripts (e.g. `SELECT status FROM orders WHERE false;`) prove a change is present; `sqitch.plan` is the ordered change log with tags.

## pgroll: zero-downtime, reversible PostgreSQL migrations
Migrations are JSON/YAML operations; pgroll runs expand/contract automatically: creates the new column/table version, backfills, keeps old and new in sync with triggers, and exposes both schema versions via views in versioned schemas so old and new app versions run concurrently.
```bash
pgroll init --postgres-url "$DB_URL"
pgroll start migrations/03_add_status.json      # expand: both versions available
# deploy new app version using search_path=public_03_add_status
pgroll complete                                  # contract: remove old version
pgroll rollback                                  # instead of complete, undo
```

## Choosing
| Need | Tool |
|---|---|
| Desired-state schema as code, linting, many engines | Atlas |
| Hand-written SQL, dependencies, verify steps | Sqitch |
| PostgreSQL zero-downtime with automatic transition period | pgroll |
| ORM-centred team | ORM migrations, with Atlas/squawk lint |

## Verify
In CI, apply then revert/rollback each change on a disposable database and confirm the schema returns to its prior state (diff dumps), and lint passes.
