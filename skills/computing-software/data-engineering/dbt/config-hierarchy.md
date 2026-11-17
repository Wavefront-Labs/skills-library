---
id: computing-software.data-engineering.dbt.config-hierarchy
name: config-hierarchy
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-config-hierarchy, dbt-project-yml, plus-prefix, config-block, properties-yml, model-configs, folder-configs, dbt-project-structure]
level: practitioner
status: verified
description: "Set dbt configs at the right level: dbt_project.yml folder configs with + prefix, properties YAML, config() blocks, precedence, and merge behaviour for tags/meta/grants."
sources:
  - https://docs.getdbt.com/reference/configs-and-properties
  - https://docs.getdbt.com/reference/model-configs
  - https://docs.getdbt.com/reference/resource-configs/plus-prefix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt config hierarchy

**Goal:** set defaults once per folder and override only where needed, so behaviour is predictable across hundreds of models.

## Three places, most specific wins
1. `config()` block in the model SQL (highest)
2. `config:` under the model in a properties `.yml` file
3. `dbt_project.yml` folder paths (lowest; deeper paths beat shallower)

```yaml
# dbt_project.yml
models:
  acme:
    +materialized: view
    staging:
      +schema: staging
      +tags: ["staging"]
    marts:
      +materialized: table
      finance:
        +schema: finance
        +grants: {select: ["role_finance_readers"]}
```
```sql
-- models/marts/finance/fct_revenue.sql
{{ config(materialized='incremental', unique_key='revenue_id', on_schema_change='append_new_columns') }}
```
```yaml
# models/marts/finance/_finance__models.yml
models:
  - name: fct_revenue
    config:
      contract: {enforced: true}
      meta: {owner: "finance-data"}
```

## The `+` prefix
In `dbt_project.yml`, `+` marks a key as a config rather than a sub-folder name. Required when a config name could collide with a folder (`+schema`, `+tags`); use it always for clarity.

## Merge vs override
- Most configs **override** (the most specific value wins): `materialized`, `schema`, `unique_key`.
- `tags` accumulate (`['proj', 'yml', 'model']` when set at project, YAML and SQL levels) and `meta` dicts merge key by key with the more specific value winning (`{a:1,b:1}` + `{b:2,c:3}` + `{c:9,d:4}` gave `a=1,b=2,c=3,d=4`; the `config()` block won over YAML). Checked on dbt 1.12.6.
- `grants` merge by privilege: a project-level `select: [r1]` was **replaced** by a model-level `select: [r2]`; write `"+select": [r2]` to append (gave `[r1, r2]`), and a different privilege (`insert`) is added alongside.
- `pre-hook`/`post-hook` accumulate from all levels (project hooks run too; checked, in project, YAML, SQL order).

## Checking the effective config
```bash
dbt ls -s fct_revenue --output json --output-keys config | jq .
dbt compile -s fct_revenue
```
Or inspect `target/manifest.json` (`nodes["model.acme.fct_revenue"].config`).

## Gotchas
- Folder keys must match the **project name** then directory names exactly; a typo applies nothing and dbt warns at parse ("Configuration paths exist in your dbt_project.yml file which do not apply to any resources", listing `models.acme.typo_folder`; checked): read the warnings.
- Package models are configured under the package name in your `dbt_project.yml`.

## Verify
- [ ] `dbt parse` shows no "Configuration paths exist in your dbt_project.yml file which do not apply to any resources".
- [ ] `dbt ls --output json` shows expected materialization/schema for a sample of models.
