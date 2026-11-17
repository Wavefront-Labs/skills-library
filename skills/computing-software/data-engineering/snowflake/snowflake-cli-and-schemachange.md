---
id: computing-software.data-engineering.snowflake.snowflake-cli-and-schemachange
name: snowflake-cli-and-schemachange
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-cli, schemachange, database-change-management, versioned-migrations, connections-toml, ci-cd, terraform-snowflake, declarative-ddl]
level: advanced
status: docs-checked
description: "Deploy Snowflake objects from git: Snowflake CLI connections and SQL execution, schemachange versioned/repeatable scripts with change history, and where Terraform fits."
sources:
  - https://docs.snowflake.com/en/developer-guide/snowflake-cli/index
  - https://github.com/Snowflake-Labs/schemachange
  - https://registry.terraform.io/providers/Snowflake-Labs/snowflake/latest/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake CLI and schemachange deployments

**Goal:** Snowflake objects not managed by dbt (warehouses, roles, stages, tasks, procedures, raw tables) are created and changed through reviewed code, not ad-hoc worksheets.

## Snowflake CLI (`snow`)
```toml
# ~/.snowflake/connections.toml
[connections.prod]
account = "<org>-<account>"
user = "svc_deploy"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "/secrets/deploy_key.p8"
role = "deployer"
warehouse = "deploy_xs"
```
```bash
snow sql -q "show warehouses"
```
Select the connection with the `snow` connection options; command syntax for sql, stage and snowpark is in the Snowflake CLI docs.

## schemachange (versioned migrations)
```
migrations/
  V1.1.0__create_raw_schema.sql
  V1.2.0__add_orders_table.sql
  R__views_reporting.sql          # repeatable: re-applied when content changes
```
```bash
schemachange deploy -f migrations -C prod \
  --change-history-table METADATA.SCHEMACHANGE.CHANGE_HISTORY --create-change-history-table
```
- Versioned scripts run once, in order; history recorded in the change history table. Never edit an applied V script: add a new one.
- Jinja variables (`{{ env }}`) for environment-specific names via `--vars`.
- `--dry-run` in PR pipelines.

## One owner per object
Don't manage the same object in two tools (for example schemachange and Terraform).

## CI/CD flow
PR: lint SQL and test migrations against a clone of prod (`create database prod_clone clone prod`). Merge: deploy to staging, then prod with approval. Service user with key-pair, role scoped to deploy permissions.

## Verify
- [ ] Change history table lists every applied script with checksums.
- [ ] A fresh environment can be rebuilt from scripts alone.

## Checked
2026-10-28. Confirmed against the schemachange README (V and R script naming, --vars, --dry-run, --change-history-table, --create-change-history-table, -C connection option, connections.toml with authenticator snowflake_jwt and private_key_file, snow sql -q). Removed: snow connection test, snow stage copy and snow snowpark deploy commands, the Streamlit and Native Apps remark, A__ always scripts, --config-folder, --connection-name and the Terraform provider paragraph, none of which were confirmed from readable sources.
Method: documentation only; no commands were run.
