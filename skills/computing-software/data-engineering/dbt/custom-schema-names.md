---
id: computing-software.data-engineering.dbt.custom-schema-names
name: custom-schema-names
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, generate-schema-name, custom-schema, generate-alias-name, generate-database-name, schema-naming, dev-schemas, environments]
level: practitioner
status: verified
description: "Control where dbt builds objects: default generate_schema_name concatenation, the env-aware override (exact schema in prod, prefixed in dev), aliases and database overrides."
sources:
  - https://docs.getdbt.com/docs/build/custom-schemas
  - https://docs.getdbt.com/docs/build/custom-aliases
  - https://docs.getdbt.com/docs/build/custom-databases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom schema names (generate_schema_name)

**Goal:** prod builds land in clean schemas (`finance`, `marketing`) while each developer and CI run builds in isolated schemas, with no collisions.

## Default behaviour (surprises people)
With `+schema: finance` and target schema `analytics`, dbt builds into **`analytics_finance`**, not `finance`. The default macro concatenates `<target.schema>_<custom_schema>` so dev users (`dbt_alice`) get `dbt_alice_finance`.

## Common override: exact in prod, prefixed elsewhere
```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- elif target.name == 'prod' -%}
        {{ custom_schema_name | trim }}
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
```
dbt also ships `generate_schema_name_for_env`, but it is **not** the same pattern: it returns the custom schema alone in prod and just `target.schema` everywhere else (the custom schema is dropped outside prod; macro source and `dbt ls` output on 1.12.6: dev `main`, prod `finance`). Use the macro above if you want `<target>_<custom>` in dev.

## Aliases and databases
- `+alias: orders` sets the table name independent of the file name (`fct_orders_v2.sql` -> `orders`). Two models resolving to the same schema+alias error at parse ("dbt found two resources with the database representation", checked).
- `generate_alias_name` macro customises naming globally (e.g. version suffixes for model versions).
- `+database:` and `generate_database_name` for multi-database layouts (Snowflake/Databricks catalogs), same concatenation caveats.

## CI
Set the CI target schema to something unique (`dbt_ci_pr_1234`), so with the override CI objects land in `dbt_ci_pr_1234_finance` etc.; clean them up afterwards.

## Gotchas
- Changing this macro on an existing project moves every object on next run: old schemas linger (drop them) and grants/BI connections must be updated.
- Snapshots in 1.9+ YAML config use `schema` + this macro (a snapshot with `schema: snapshots` landed in `main_snapshots`); a legacy `{% snapshot %}` with `target_schema='legacy_s'` landed in `legacy_s` unchanged.
- Package models are also routed through your macro.

## Verify
- [ ] `dbt ls -s marts --output json --output-keys "schema alias"` with `--target prod` and `--target dev` shows the intended names.
- [ ] No dev target can write to a prod schema (role permissions back this up).
