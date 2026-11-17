---
id: computing-software.software-engineering.quarkus.quarkus-hibernate-orm-schema-and-data-init
name: quarkus-hibernate-orm-schema-and-data-init
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, hibernate-orm, schema-management, data-sql, dev-mode, flyway]
level: practitioner
status: docs-checked
description: "Control Hibernate ORM schema generation and data.sql/import.sql in Quarkus across dev, test and prod using schema-management and data-management strategies and profiles."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/hibernate-orm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hibernate ORM schema and data initialisation in Quarkus

## Init scripts (resources root)
- `schema.sql`: completes the generated schema with objects Hibernate cannot generate (constraints, views, functions). Runs only when Hibernate creates the schema (`quarkus.hibernate-orm.schema-management.strategy` is `create` or `drop-and-create`), before `data.sql`. Override with `quarkus.hibernate-orm.schema-management.init-script`.
- A legacy `import.sql` enables a deprecated dev/test-only behavior (executed whenever Hibernate creates the schema; it cannot be combined with `schema.sql`, `data.sql`, the script properties or `data-management.strategy`). Move its statements to `data.sql` (data) and/or `schema.sql` (schema objects), then delete it.
- `data.sql`: loads reference/test data. By default runs in dev and test only. `quarkus.hibernate-orm.data-management.strategy` = `none` disables it, `create` runs it in production too; `quarkus.hibernate-orm.data-management.init-script` picks other files (a `.zip` of SQL files also works).
- End every statement with a semicolon.
- If Hibernate does not create the schema (Flyway/Liquibase), `data.sql` runs on every start, including each dev live reload. Make it idempotent (`MERGE`, `INSERT ... ON CONFLICT`) or set the strategy to `none`.

## Dev/test choices
1. `schema-management.strategy=drop-and-create` plus `data.sql`: schema rebuilt and data reloaded on every change; works with live reload (the default with Dev Services).
2. `update`: best effort, can fail or lose data on structural changes; good for working on a copy of production data. `data.sql` still runs each startup.
3. `none` (optionally `validate`): you manage the schema yourself or via Flyway/Liquibase.

## Production defaults
`schema-management.strategy` and `data-management.strategy` default to `none` for every profile except `dev` and `test`. Do not set `drop-and-create` or `update` in production. Make it explicit:

```properties
%dev.quarkus.hibernate-orm.schema-management.strategy = drop-and-create
%dev.quarkus.hibernate-orm.data-management.init-script = data-dev.sql
%dev-with-data.quarkus.hibernate-orm.schema-management.strategy = update
%dev-with-data.quarkus.hibernate-orm.data-management.strategy = none
%prod.quarkus.hibernate-orm.schema-management.strategy = none
%prod.quarkus.hibernate-orm.data-management.strategy = none
```

Start a custom profile with `-Dquarkus.profile=dev-with-data`.

## Moving to Flyway
With `quarkus-flyway` in dev mode, the Dev UI Flyway pane's `Create Initial Migration` button writes `db/migration/V1.0.0__{appname}.sql` from the Hibernate schema and sets `quarkus.flyway.baseline-on-migrate`, `quarkus.flyway.migrate-at-start` and `%dev`/`%test` `clean-at-start`. `Generate Migration File` drafts later migrations; always review them.

## Checked

2026-11-07. Read in full: hibernate-orm.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the claim that `import.sql` completes the schema, the claim that Quarkus requires semicolons because Hibernate defaults to one statement per line, and the warning that a data script named `import.sql` runs twice. The page now documents `schema.sql`, and describes `import.sql` as a deprecated legacy behavior.

Method: documentation only; no commands were run.
