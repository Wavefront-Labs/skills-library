---
id: computing-software.data-engineering.dbt.hooks-and-operations
name: hooks-and-operations
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-hooks, pre-hook, post-hook, on-run-start, on-run-end, results-object, grants, audit-logging]
level: practitioner
status: gated
description: "Use dbt hooks: model pre_hook/post_hook, project on-run-start/on-run-end with the results object, transaction behaviour, and replacing grant hooks with the grants config."
sources:
  - https://docs.getdbt.com/reference/resource-configs/pre-hook-post-hook
  - https://docs.getdbt.com/reference/project-configs/on-run-start-on-run-end
  - https://docs.getdbt.com/reference/dbt-jinja-functions/on-run-end-context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hooks and operations

**Goal:** run SQL around model builds or whole invocations (housekeeping, audit logging, session settings) without hiding logic in odd places.

## Model hooks
```sql
{{ config(
    post_hook=[
      "alter table {{ this }} cluster by (event_date)",
      "{{ log_model_run(this) }}"
    ],
    pre_hook="alter session set query_tag = 'dbt:{{ model.name }}'"   -- Snowflake syntax (gated: unconfirmed, source is paywalled or blocked)
) }}
```
- Hooks from project, folder and model levels all run (they accumulate; resolved order was project, YAML, then SQL `config()`, checked).
- On adapters with transactions (Postgres/Redshift), hooks run inside the model's transaction by default; use `{"sql": "vacuum ...", "transaction": false}` (or `before_begin()`/`after_commit()`) for statements that cannot run in a transaction (gated: unconfirmed, source is paywalled or blocked). The resolved config does carry a `transaction: True` flag per hook (checked).

## Invocation hooks
```yaml
# dbt_project.yml
on-run-start:
  - "create schema if not exists {{ target.schema }}_audit"
on-run-end:
  - "{{ log_run_results(results) }}"
```
```sql
{% macro log_run_results(results) %}
  {% if execute %}
    {% for r in results %}
      {% do run_query("insert into audit.dbt_runs values ('" ~ invocation_id ~ "','" ~ r.node.unique_id ~ "','" ~ r.status ~ "'," ~ (r.execution_time | round(2)) ~ ", current_timestamp)") %}
    {% endfor %}
  {% endif %}
{% endmacro %}
```
`results` is only available in `on-run-end` (the macro above wrote one `success` row per node on dbt-duckdb, checked). For richer run logging consider the `dbt_artifacts` package or parsing `run_results.json` outside dbt.

## Prefer configs over hooks where they exist
- Grants: `+grants: {select: ['reporter']}` instead of `grant select ...` post-hooks; dbt also revokes stale grants (gated: unconfirmed, source is paywalled or blocked).
- Clustering/partitioning: adapter configs (`cluster_by`, `partition_by`) instead of ALTER hooks.
- Comments: `persist_docs`.

## Gotchas
- Hooks run on every build of the model (including CI): keep them idempotent and fast.
- Failing hook = failed model.
- Jinja in `dbt_project.yml` hooks is rendered at runtime; quoting inside YAML strings gets tricky: move logic into macros.

## Verify
- [ ] `dbt run -s model --debug` shows hooks executing in the expected order.
- [ ] Audit table receives one row per node per invocation.
