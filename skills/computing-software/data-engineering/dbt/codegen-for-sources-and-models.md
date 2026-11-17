---
id: computing-software.data-engineering.dbt.codegen-for-sources-and-models
name: codegen-for-sources-and-models
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-codegen, generate-source, generate-base-model, generate-model-yaml, run-operation, scaffolding, staging-models]
level: practitioner
status: docs-checked
description: "Scaffold dbt sources, staging models and model YAML with the dbt-codegen package: generate_source, generate_base_model, generate_model_yaml, and cleaning up the output."
sources:
  - https://github.com/dbt-labs/dbt-codegen
  - https://hub.getdbt.com/dbt-labs/codegen/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaffolding with dbt-codegen

**Goal:** onboard a new source system with dozens of tables in minutes instead of hand-typing YAML and boilerplate SQL.

## Install
```yaml
# packages.yml
packages:
  - package: dbt-labs/codegen
    version: 0.14.1   # latest release on GitHub; check hub.getdbt.com for the newest
```
`dbt deps`

## 1. Source YAML from the warehouse
```bash
dbt --quiet run-operation generate_source --args '{"schema_name": "stripe", "database_name": "raw", "generate_columns": true, "include_descriptions": true}' > tmp_sources.yml
```
Paste into `models/staging/stripe/_stripe__sources.yml`; add `loaded_at_field`/freshness and key tests. `generate_columns` and `include_descriptions` both default to false.

## 2. Staging model per table
```bash
for t in charges customers refunds; do
  dbt --quiet run-operation generate_base_model --args "{\"source_name\": \"stripe\", \"table_name\": \"$t\"}" \
    > models/staging/stripe/stg_stripe__$t.sql
done
```
Output is a `source` CTE selecting from the source plus a `renamed` CTE listing every column. Then edit: rename to conventions (`id` -> `charge_id`), cast types, convert cents, drop junk columns.

## 3. Model YAML with columns
```bash
dbt run-operation generate_model_yaml --args '{"model_names": ["stg_stripe__charges", "stg_stripe__customers"], "upstream_descriptions": true}'
```
`upstream_descriptions` includes descriptions for identical column names from upstream models and sources.

## Tips
- `--quiet` is a global flag placed before `run-operation` (`dbt --quiet run-operation ...`) so log lines stay out of the redirected file.
- Codegen output is a draft: the value is in your edits (naming, typing, tests).
- Also: `generate_model_import_ctes` to refactor legacy SQL into import CTEs.

## Verify
- [ ] Generated files compile (`dbt compile -s source:stripe+`).
- [ ] Every new staging model has renamed keys and a uniqueness test on its primary key.

## Checked

2026-10-25: dbt-codegen README on main. Confirmed: dbt-codegen README (repository last commit 2026-10-01, latest release 0.14.1): macros generate_source (arguments schema_name, database_name, table_names, generate_columns default false, include_descriptions default false), generate_base_model (source_name, table_name; source and renamed CTEs), generate_model_yaml (model_names, upstream_descriptions), generate_model_import_ctes, and the `dbt --quiet run-operation ... > file` output pattern. Removed the unconfirmed claim that models must exist in the warehouse and the version range.

Method: documentation only; no commands were run.
