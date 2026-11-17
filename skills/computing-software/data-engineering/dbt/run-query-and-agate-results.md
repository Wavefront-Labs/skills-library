---
id: computing-software.data-engineering.dbt.run-query-and-agate-results
name: run-query-and-agate-results
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-macros, run-query, agate, execute-flag, statement-blocks, dynamic-sql, introspection]
level: advanced
status: verified
description: "Run queries from dbt macros with run_query, read agate tables (columns, rows, values), guard with execute, and generate dynamic SQL without breaking parsing."
sources:
  - https://docs.getdbt.com/reference/dbt-jinja-functions/run_query
  - https://docs.getdbt.com/reference/dbt-jinja-functions/execute
  - https://docs.getdbt.com/reference/dbt-classes#agate-table
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# run_query and agate results

**Goal:** query the warehouse during compilation to drive SQL generation (pivot columns, list of partitions to process) safely.

## Basic pattern
```sql
{% macro get_payment_methods() %}
  {% set q %}
    select distinct payment_method from {{ ref('stg_payments') }} order by 1
  {% endset %}
  {% set results = run_query(q) %}
  {% if execute %}
    {% set methods = results.columns[0].values() %}
  {% else %}
    {% set methods = [] %}
  {% endif %}
  {{ return(methods) }}
{% endmacro %}
```
```sql
select order_id,
  {% for m in get_payment_methods() %}
  sum(case when payment_method = '{{ m }}' then amount end) as {{ m | lower }}_amount{% if not loop.last %},{% endif %}
  {% endfor %}
from {{ ref('stg_payments') }} group by 1
```

## Why `execute`
dbt parses every model first without running queries (`execute = False`). At parse time `run_query` returns a placeholder that is not an agate table (`r is none` was false); using `.columns` on it raised `'None' has no attribute 'table'` (dbt 1.12.6). Always branch on `execute` and return a harmless default.

## Working with the agate table
```jinja
{% set t = run_query("select table_name, row_count from info.tables") %}
{% if execute %}
  {% for row in t.rows %}  {{ log(row['table_name'] ~ ': ' ~ row['row_count'], info=true) }}  {% endfor %}
  {% set first_val = t.columns['row_count'].values()[0] %}
  {% set n = t.rows | length %}
  {% do t.print_table() %}          {# debug printing to stdout #}
{% endif %}
```
- Column names are as returned by the warehouse (lowercase on DuckDB; match your adapter's case). The example above ran on DuckDB and printed a table from `print_table()`.
- Values come back as Python types; cast/format before injecting into SQL.

## Shortcut helpers
`dbt_utils.get_column_values(table=ref('x'), column='status')` (arguments `table`, `column`, `where`, `order_by`, `max_records`, `default`) and `dbt_utils.get_query_results_as_dict(sql)` wrap this pattern (dbt-utils README).

## Gotchas
- Every `run_query` is a round-trip at compile time; in loops over many models this slows `dbt compile`/`build` and dbt Cloud IDE.
- Dynamic column lists change model schema as data changes: add a contract or accepted-values test so a new category does not silently add columns downstream.
- `run_query` runs on the target connection with the model's privileges; in CI on empty schemas results are empty, so defaults must still compile.
- Do not use it for DDL/DML in models; use hooks or `run-operation` macros.

## Verify
- [ ] `dbt parse` succeeds (no None errors).
- [ ] `dbt compile -s model` shows expected generated columns in `target/compiled`.
