---
id: computing-software.data-engineering.data-modelling.versioned-schema-migrations
name: versioned-schema-migrations
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, schema-migration, flyway, liquibase, versioned-migrations, changelog, rollback, baseline, database-ci-cd, schema-drift]
level: practitioner
status: gated
description: "Manage DDL changes with versioned migrations: Flyway V/R scripts and Liquibase changelogs, baselining an existing database, CI validation, rollbacks, and detecting schema drift."
sources:
  - https://docs.liquibase.com/concepts/changelogs/home.html
  - https://www.dama.org/cpages/body-of-knowledge
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Versioned schema migrations (Flyway, Liquibase)

**Goal:** every schema change is a reviewed, ordered, repeatable script, applied identically to every environment, with a record of what ran where.

## Flyway
```
sql/
  V1__create_orders.sql
  V2__add_orders_channel.sql
  V2.1__index_orders_customer.sql
  R__vw_order_summary.sql          # repeatable: re-run when checksum changes (views, procs)
```
```bash
flyway -url=jdbc:postgresql://<HOST>/shop -user=$U -password=$P -locations=filesystem:sql info
flyway ... migrate
flyway ... validate          # fails if applied scripts were edited (checksum mismatch)
```
History lives in `flyway_schema_history`. Never edit an applied V script; add a new version.

## Liquibase
```yaml
# changelog.yaml
databaseChangeLog:
  - changeSet:
      id: 2026-10-16-add-channel
      author: data-platform
      changes:
        - addColumn:
            tableName: orders
            columns: [{column: {name: channel, type: varchar(20)}}]
      rollback:
        - dropColumn: {tableName: orders, columnName: channel}
```
The Liquibase commands `update`, `rollback-count`, `update-sql`, `generate-changelog` and `changelog-sync` all appear in the Liquibase command reference; Flyway and Liquibase were not installed or run here (Java 8 only, no Flyway download from Maven) and the Flyway documentation pages could not be fetched (gated: unconfirmed, source is paywalled or blocked).
`liquibase update`, `liquibase rollback-count 1`, `liquibase update-sql` (preview SQL), `liquibase diff` (compare two databases). History in `DATABASECHANGELOG`.

## Existing databases
Baseline: generate the current DDL as V1 (`flyway baseline -baselineVersion=1` marks it applied without running) or `liquibase generate-changelog` + `changelog-sync`.

## CI/CD
1. PR: run all migrations against an ephemeral database (container) from scratch + `validate`.
2. Apply to staging, run app/pipeline tests.
3. Prod deploy by pipeline only, with a backup/snapshot first for destructive changes.
- Rollback strategy: write forward-fix migrations for most cases; explicit rollbacks for risky changes; destructive changes (drops) go through expand-contract.

## Drift
Manual hotfixes in prod cause drift: detect with `liquibase diff`/Flyway's `check -drift` (Redgate editions) or a scheduled comparison of `information_schema` against a fresh migration build.

## Verify
- [ ] Fresh database built from migrations matches prod schema (diff empty).
- [ ] `validate` passes in CI; edited applied scripts are rejected.
