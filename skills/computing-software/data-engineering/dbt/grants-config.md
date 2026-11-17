---
id: computing-software.data-engineering.dbt.grants-config
name: grants-config
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-grants, grants-config, access-control, revoke, future-grants, copy-grants, least-privilege, bi-access]
level: practitioner
status: docs-checked
description: "Manage warehouse access from dbt with the grants config: select grants per folder or model, revoking, the + prefix for adding grantees, and adapter notes including copy_grants."
sources:
  - https://docs.getdbt.com/reference/resource-configs/grants
  - https://docs.getdbt.com/reference/resource-configs/snowflake-configs#copying-grants
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Grants config

**Goal:** the right roles can read each model immediately after every rebuild, defined next to the model, without hand-run GRANT statements.

## Configure
```yaml
# dbt_project.yml
models:
  acme:
    marts:
      +grants:
        select: ['reporter']
      finance:
        +grants:
          select: ['finance_analyst']     # replaces the inherited list for this folder (more specific config wins)
```
```sql
{{ config(grants={'+select': ['finance_analyst']}) }}   -- model level: the + prefix on the privilege adds to the inherited list; without it the list is replaced
```
Keys are privilege names (`select`, ...); values are grantees as the warehouse expects. BigQuery uses roles such as `roles/bigquery.dataViewer` as keys and grantees like `user:someone@yourcompany.com`; Redshift treats unprefixed names as users (use `group:` or `role:`).

## Behaviour
- On later runs dbt shows the grants already on the relation and issues the `grant`/`revoke` statements needed to match the config. `select: []` revokes all.
- dbt only modifies grants on a node (including revocation) when a `grants` config is attached; deleting the whole `+grants` section makes dbt stop managing grants.
- Support varies: OSS Apache Spark and Delta Lake do not support `grants`; on Databricks use post-hooks to grant `READ_METADATA` or `USAGE`; on Snowflake grant/revoke is fully supported only for roles, not database roles.
- On Snowflake dbt accounts for the `copy_grants` config when calculating which grants to add or remove.



## Verify
- [ ] The grants shown by the warehouse for the relation match the config after a rebuild.
- [ ] Grants are defined in config, not by hand.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt grants config page: `grants` in YAML properties, project file or `config()`, inheritance replacing less-specific grantees, `+` prefix on the privilege to add instead of replace, conditional grants with Jinja, revoking with an empty list or by removing the config, adapter notes for BigQuery roles and prefixes, Databricks (OSS Spark/Delta unsupported, post-hooks for READ_METADATA/USAGE), Redshift prefixes and Snowflake copy_grants and role limits. Removed unconfirmed claims about CREATE OR REPLACE behaviour and warehouse-level grant alternatives.

Method: documentation only; no commands were run.
