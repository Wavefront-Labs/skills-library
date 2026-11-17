---
id: computing-software.data-engineering.dbt.jinja-control-flow-and-whitespace
name: jinja-control-flow-and-whitespace
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, jinja, jinja-control-flow, for-loop, set-block, whitespace-control, namespace, dbt-macros]
level: practitioner
status: verified
description: "Write clean Jinja in dbt: for loops with loop.last, set and set blocks, namespace() for loop accumulators, whitespace control, filters, and readable compiled SQL."
sources:
  - https://docs.getdbt.com/docs/build/jinja-macros
  - https://jinja.palletsprojects.com/en/3.1.x/templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jinja control flow and whitespace in dbt

**Goal:** Jinja that compiles to valid, readable SQL, and avoids the classic scoping and comma bugs.

## Loops and trailing commas
```sql
{% set metrics = ['revenue', 'cost', 'margin'] %}
select
  order_date,
  {% for m in metrics %}
  sum({{ m }}) as total_{{ m }}{{ "," if not loop.last }}
  {% endfor %}
from {{ ref('fct_orders') }}
group by 1
```
`loop.first`, `loop.last`, `loop.index` (1-based), `loop.index0` are available.

## set vs set block
```jinja
{% set cutoff = "2026-01-01" %}
{% set filter_sql %}
  where order_date >= '{{ cutoff }}' and status != 'test'
{% endset %}
select * from {{ ref('stg_orders') }} {{ filter_sql }}
```

## Loop scoping trap
Variables set inside a loop do not persist outside it:
```jinja
{% set ns = namespace(total=0, found=false) %}
{% for c in cols %}
  {% if c.name == 'amount' %}{% set ns.found = true %}{% endif %}
  {% set ns.total = ns.total + 1 %}
{% endfor %}
{{ ns.found }}
```
Plain `{% set found = true %}` inside the loop would be lost. Lists can be mutated with `{% do my_list.append(x) %}`.

## Whitespace control
`{%-` strips whitespace before, `-%}` after:
```jinja
{%- for col in cols %}
  {{ col }}{{ "," if not loop.last }}
{%- endfor %}
```
Use sparingly; readability of compiled SQL matters more than perfect whitespace.

## Useful filters and tests
`| join(', ')`, `| map(attribute='name') | list`, `| selectattr('data_type','equalto','DATE')`, `| lower`, `| replace('-', '_')`, `| default('x')`, `is none`, `is string`, `in`.
```jinja
{{ cols | map(attribute='name') | map('lower') | join(', ') }}
```

## Comments
`{# Jinja comment, not in compiled SQL #}` vs `-- SQL comment` (kept, and Jinja inside it still renders and can fail).

## Gotchas
- `{{ }}` inside a `{% %}` is wrong: `{% if var('x') == 'y' %}` not `{% if {{ var('x') }} == 'y' %}`.
- A quoted or env-sourced `'false'` is a truthy string. On dbt 1.12.6 `--vars '{flag: false}'` gave a real boolean (falsy) while `--vars 'flag: "false"'` gave the string (truthy). Normalise when the source is unknown: `var('flag', false) | string | lower == 'true'`.
- Integer division: `{{ 7 / 2 }}` rendered 3.5 and `{{ 7 // 2 }}` 3 (checked).
- Over-templating: if a model is mostly Jinja, consider a macro or a simpler model design.

## Verify
- [ ] `dbt compile` output is valid SQL with no trailing commas or blank-line soup.
- [ ] Edge cases (empty list) compile: guard `{% if cols %}`.
