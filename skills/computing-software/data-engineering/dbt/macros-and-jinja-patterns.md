---
id: computing-software.data-engineering.dbt.macros-and-jinja-patterns
name: macros-and-jinja-patterns
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-macros, jinja, dispatch, run_query, compile-time, adapter-dispatch, cross-database-macros, dbt-packages, macro-override, statement-blocks, dbt-utils]
level: advanced
status: docs-checked
description: "Write reusable dbt macros and Jinja patterns correctly: adapter dispatch, run_query side effects at compile time, package macro overrides and statement blocks."
sources:
  - https://docs.getdbt.com/docs/build/jinja-macros
  - https://docs.getdbt.com/reference/dbt-jinja-functions/run_query
  - https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch
  - https://docs.getdbt.com/reference/project-configs/dispatch-config
  - https://docs.getdbt.com/reference/dbt-jinja-functions/statement-blocks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt macros and Jinja — the parts that aren't just templating

**Goal:** write macros that are cross-database-portable and that do not run surprising queries when dbt compiles.

## 1. `run_query()` runs whenever dbt compiles with a live connection
```sql
{% set relation_columns = run_query("select column_name from information_schema.columns where table_name = 'orders'") %}
```
`run_query` is a wrapper around the statement block and returns an agate Table (or `none` when the query returns no results, such as DDL). The dbt docs warn that it runs SQL against the warehouse whenever dbt compiles your project with a live connection, including `dbt compile` and `dbt docs generate`. So side-effecting statements (DML, maintenance) inside `run_query` also run in those workflows unless you scope them, for example with `flags.WHICH`. Store a lookup in a variable once rather than calling `run_query` repeatedly for the same result.

## 2. Adapter dispatch — one macro, correct SQL per warehouse
```sql
{% macro cents_to_dollars(column_name) %}
  {{ return(adapter.dispatch('cents_to_dollars', 'my_project')(column_name)) }}
{% endmacro %}

{% macro default__cents_to_dollars(column_name) %}
  ({{ column_name }} / 100.0)
{% endmacro %}

{% macro snowflake__cents_to_dollars(column_name) %}
  ({{ column_name }}::float / 100.0)
{% endmacro %}
```
`adapter.dispatch` looks for `<adapter>__<macro_name>` and falls back to `default__<macro_name>`. If the adapter inherits from another (the docs give `dbt-spark` to `dbt-databricks`), parent adapter implementations are searched too, before `default__`. Where dbt looks is controlled by the `dispatch` config in `dbt_project.yml` (`macro_namespace` plus `search_order`); by default it looks in the root project first, then in the package named by the namespace. This is how a project overrides one adapter's variant of a package macro without touching the others.

## 3. Overriding a package's macro
Define a candidate macro (for example `default__concat` or `snowflake__concat`) in your root project and let dispatch find it first, or set `dispatch` search order explicitly. The dispatch docs describe this mechanism for packages that call `adapter.dispatch`. Check how the package macro is called (via dispatch or directly) before relying on an override, and confirm what else calls that macro.

## 4. Statement blocks for non-SELECT SQL
`{% call statement('my_statement') %} GRANT SELECT ON {{ this }} TO ROLE analyst {% endcall %}` runs arbitrary SQL inside a macro (the docs show maintenance statements such as `OPTIMIZE` with `fetch_result=False`). Keep side effects idempotent, since hooks can run on every `dbt run`.

## Verify
- [ ] Any macro using `run_query()` was checked for how many times it executes per `dbt compile` and `dbt docs generate`.
- [ ] Cross-database macros use `adapter.dispatch` rather than hand-rolled `target.type` branching.
- [ ] An overridden package macro was reviewed against its callers before the override shipped.
- [ ] Any statement-block DDL is idempotent under a repeated `dbt run`.

## Checked
2026-11-01. Confirmed against the dbt docs repo (docs.getdbt.com): run_query compile-time behaviour and return value, dispatch naming (`<adapter>__`, `default__`), parent-adapter search, and the dispatch config default search order; statement-block `call statement` usage. Removed: unconfirmed parse-time versus relation-cache claims, the claim that local macros always shadow package macros globally, and the dbt_expectations portability claim.
Method: documentation only; no commands were run.
