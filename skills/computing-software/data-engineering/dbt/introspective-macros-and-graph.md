---
id: computing-software.data-engineering.dbt.introspective-macros-and-graph
name: introspective-macros-and-graph
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-macros, introspective-queries, graph-variable, get-relations-by-pattern, adapter-get-columns-in-relation, union-relations, dbt-utils]
level: advanced
status: docs-checked
description: "Write dbt macros that introspect the project graph and the warehouse: graph.nodes, adapter.get_columns_in_relation, get_relations_by_pattern and union_relations."
sources:
  - https://docs.getdbt.com/reference/dbt-jinja-functions/graph
  - https://docs.getdbt.com/reference/dbt-jinja-functions/adapter
  - https://docs.getdbt.com/reference/dbt-jinja-functions/statement-blocks
  - https://github.com/dbt-labs/dbt-utils#introspective-macros
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Introspective macros and the graph

**Goal:** generate SQL from metadata: union all shard tables matching a pattern, select all columns except a few, or find models by package, without hard-coding lists.

## Warehouse introspection
```sql
{% set rel = ref('stg_orders') %}
{% set cols = adapter.get_columns_in_relation(rel) %}        {# list of Column objects #}
select
  {% for c in cols if c.name | lower not in ['_loaded_at', '_file'] %}
  {{ adapter.quote(c.name) }}{% if not loop.last %},{% endif %}
  {% endfor %}
from {{ rel }}
```
`dbt_utils.star(from=ref('stg_orders'), except=['_loaded_at'])` generates the same comma-separated column list (note: `quote_identifiers` defaults to true).

## Union tables matching a pattern
```sql
{% set shards = dbt_utils.get_relations_by_pattern('raw_shopify%', 'orders') %}
{{ dbt_utils.union_relations(relations=shards) }}
```
`union_relations` combines the relations with `union all` even when column order differs or some columns are missing (missing columns are filled with null) and adds a `_dbt_source_relation` column (name set by `source_column_name`, `None` omits it).

## The graph variable
```jinja
{% macro models_in_package(package) %}
  {% set out = [] %}
  {% if execute %}
    {% for node in graph.nodes.values()
         | selectattr('resource_type', 'equalto', 'model')
         | selectattr('package_name', 'equalto', package) %}
      {% do out.append(node.unique_id) %}
    {% endfor %}
  {% endif %}
  {{ return(out) }}
{% endmacro %}
```
The `graph` variable holds `nodes`, `sources`, `exposures` and `metrics`. The exact node contract is not documented, entries for models are incomplete during parsing, and `graph` must not be used to build the DAG, so read it only when `execute` is true.

## Lineage caveat
A `ref` or `source` inside a macro creates a dependency; relations found only by introspection are not known to the DAG. Inside `statement` blocks, dbt cannot infer a dependency on a model you do not `ref` elsewhere: add a `-- depends_on: {{ ref('x') }}` comment.

## Gotchas
- Introspection and `graph` access belong behind `{% if execute %}`: during parsing the graph is incomplete and queries have not run.
- `adapter.get_columns_in_relation` returns the Column objects of a relation in the warehouse, so the relation must exist when the macro runs.

## Verify
- [ ] `dbt compile` output shows the expected union/columns.

## Checked

2026-10-25: dbt docs and dbt-utils README. Confirmed: dbt Jinja `graph`, `adapter.get_columns_in_relation`, `execute` and statement-blocks docs, and the dbt-utils README (repository last commit 2026-10-01): `get_relations_by_pattern(schema_pattern, table_pattern, exclude)`, `union_relations` behaviour and `source_column_name` default `_dbt_source_relation`, `star(from, except, ...)`, `graph` structure and parse-phase caveat, `-- depends_on` comment in statement blocks. Replaced the invalid `contains` tag filter with the documented `package_name` filter and removed unconfirmed claims about parse-time column lists and information_schema performance.

Method: documentation only; no commands were run.
