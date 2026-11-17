---
id: computing-software.data-engineering.dbt.run-operation-admin-macros
name: run-operation-admin-macros
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, run-operation, admin-macros, drop-stale-models, cleanup-schemas, ci-schema-cleanup, macro-args, warehouse-housekeeping]
level: advanced
status: gated
description: "Run warehouse admin tasks with dbt run-operation: macro args, dropping orphaned relations not in the manifest, cleaning CI schemas, and dry-run safeguards."
sources:
  - https://docs.getdbt.com/reference/commands/run-operation
  - https://docs.getdbt.com/reference/dbt-jinja-functions/graph
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# run-operation for admin tasks

**Goal:** use the project's connection and context (target, graph) to perform housekeeping that is not a model build.

## Invoke
```bash
dbt run-operation drop_orphaned_relations --args '{"schemas": ["analytics", "staging"], "dry_run": true}'
```
The macro runs once; use `run_query` / `statement` inside it. `--args` is YAML/JSON.

## Example: drop relations no longer produced by the project
```sql
{% macro drop_orphaned_relations(schemas, dry_run=true) %}
  {% set expected = [] %}
  {% for n in graph.nodes.values() if n.resource_type in ['model', 'seed', 'snapshot'] %}
    {% do expected.append((n.schema | lower) ~ '.' ~ (n.alias or n.name) | lower) %}
  {% endfor %}
  {% for s in schemas %}
    {% set rels = run_query("select table_name, table_type from " ~ target.database ~ ".information_schema.tables where lower(table_schema) = '" ~ s | lower ~ "'") %}
    {% for row in rels %}
      {% set fq = s | lower ~ '.' ~ row[0] | lower %}
      {% if fq not in expected %}
        {% set kind = 'view' if row[1] == 'VIEW' else 'table' %}
        {% set sql = 'drop ' ~ kind ~ ' if exists ' ~ target.database ~ '.' ~ fq %}
        {{ log(('DRY RUN: ' if dry_run else '') ~ sql, info=true) }}
        {% if not dry_run %}{% do run_query(sql) %}{% endif %}
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endmacro %}
```
Renamed/deleted models leave stale tables that BI tools keep querying; run this weekly with `dry_run` reviewed first. Checked on DuckDB with `--args '{"schemas": ["main"], "dry_run": true}'` after replacing the `<db>.information_schema.tables` reference with plain `information_schema.tables` (DuckDB has no per-database information schema): it listed the orphaned seed tables. The `table_type` value `VIEW` matched.

## Example: clean CI schemas
```sql
{% macro drop_ci_schemas(prefix='dbt_ci_pr_', older_than_days=3) %}
  {% set q %}
    select schema_name from {{ target.database }}.information_schema.schemata
    where schema_name ilike '{{ prefix }}%' and created < dateadd(day, -{{ older_than_days }}, current_timestamp)
  {% endset %}
  {% for s in run_query(q).columns[0].values() %}
    {% do run_query('drop schema if exists ' ~ target.database ~ '.' ~ s ~ ' cascade') %}
    {{ log('dropped ' ~ s, info=true) }}
  {% endfor %}
{% endmacro %}
```
(This second macro uses Snowflake information-schema columns (`created`, `ilike`, `dateadd`) and was not run (gated: unconfirmed, source is paywalled or blocked). Information schema layout differs by adapter: adjust per warehouse or use `adapter.list_relations_without_caching`.)

## Safety
- Default to `dry_run=true`; require an explicit flag to execute.
- Run with a role that can only drop in the intended schemas.
- `graph` is populated at execution time; wrap graph-dependent logic with `{% if execute %}` when called from models.

## Verify
- [ ] Dry run lists only genuinely orphaned relations.
- [ ] After execution, `dbt build` still succeeds (nothing needed was dropped).
