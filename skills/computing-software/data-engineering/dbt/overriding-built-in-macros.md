---
id: computing-software.data-engineering.dbt.overriding-built-in-macros
name: overriding-built-in-macros
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, builtin-macro-override, adapter-dispatch, generate-schema-name, macros]
level: sme
status: docs-checked
description: "Override dbt built-in and package macros safely: root-project overrides (generate_schema_name, ref), adapter dispatch prefixes, and dispatch search_order for packages."
sources:
  - https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch
  - https://docs.getdbt.com/docs/build/custom-schemas
  - https://docs.getdbt.com/reference/dbt-jinja-functions/builtins
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overriding built-in macros

**Goal:** change dbt's default behaviour (schema naming, relation rendering, materialization SQL) without forking dbt or packages.

## Root project wins for global macros
Define a macro with the same name in your project's `macros/`:
```sql
{% macro generate_schema_name(custom_schema_name, node) -%}
  {%- if target.name == 'prod' and custom_schema_name -%}{{ custom_schema_name | trim }}
  {%- else -%}{{ target.schema }}{% if custom_schema_name %}_{{ custom_schema_name | trim }}{% endif %}
  {%- endif -%}
{%- endmacro %}
```
`generate_schema_name` is one such dispatched global macro (see the custom schemas page).

## Wrapping ref/source
```sql
{% macro ref() %}
  {% set rel = builtins.ref(*varargs, **kwargs) %}
  {% do return(rel.include(database=(target.name == 'prod'))) %}
{% endmacro %}
```
Delegate to `builtins.ref` and handle both the one-argument and the package-plus-model (two positional arguments) forms via `varargs`.

## Adapter-specific implementations
Adapter-specific macros are prefixed with the lowercase adapter name and two underscores: for `my_macro`, dbt looks for `<adapter>__my_macro`, then `default__my_macro`. Define an adapter-prefixed version (for example `spark__generate_schema_name`) to override for one adapter.

## Packages: dispatch search order
```yaml
# dbt_project.yml
dispatch:
  - macro_namespace: dbt_utils
    search_order: ['my_project', 'dbt_utils']
```
Now a dispatched `dbt_utils` macro such as `concat` is searched first as `my_project.<adapter>__concat`, then `my_project.default__concat`, then in `dbt_utils`.

## Gotchas
- Overrides apply to every model: a schema macro change in prod can create new schemas and orphan old ones. Compare relation names before and after.
- Copy the current upstream implementation as your starting point and re-check after upgrades.
- Macro name typos create a new, unused macro silently.

## Verify
`dbt compile` output shows the changed SQL/relation names.

## Checked
2026-11-01. Confirmed against the dbt dispatch, builtins and custom schemas pages: root-project override by name, adapter prefix and `default__` lookup, `dispatch` config with `search_order`, `builtins.ref` and `varargs`, `rel.include(database=...)`. Removed: `generate_alias_name`/`generate_database_name`/`get_custom_alias` list, `kwargs` claim, `dbt ls --output-keys` command and `dbt run-operation` verification (not on those pages).
Method: documentation only; no commands were run.
