---
id: computing-software.data-engineering.dbt.custom-materializations
name: custom-materializations
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, custom-materialization, materialization-macro, adapter-macros, load-relation, statement-call, run-hooks, dbt-materializations]
level: sme
status: docs-checked
description: "Write a custom dbt materialization: the materialization macro skeleton, relations and statement('main'), hooks and transactions, returning relations, and when not to do this."
sources:
  - https://docs.getdbt.com/guides/create-new-materializations
  - https://github.com/dbt-labs/dbt-adapters/tree/main/dbt-adapters/src/dbt/include/global_project/macros/materializations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom materializations

**Goal:** encode a repeatable build pattern the built-ins do not provide (e.g. swap-based table builds, insert-only append with audit, external tables), once, for many models.

## First, check you need one
Most needs are covered by incremental strategies, `pre_hook`/`post_hook`, or a package. Custom materializations are code you own across dbt upgrades.

## Skeleton
```sql
{%- materialization my_view, default -%}

  {%- set target_relation = api.Relation.create(
        identifier=this.identifier, schema=this.schema, database=this.database,
        type='view') -%}

  -- ... setup database ...
  {{ run_hooks(pre_hooks) }}

  -- build model
  {% call statement('main') -%}
    {{ create_view_as(target_relation, sql) }}
  {%- endcall %}

  {{ run_hooks(post_hooks) }}
  -- ... clean up the database, then {{ adapter.commit() }} ...

  -- Return the relations created in this materialization
  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}
```
Use in a model: `{{ config(materialized='my_view') }}`. The block is `{% materialization <name>, <adapter name | default> %}`; dbt picks the one for the active adapter and falls back to `default`.

## Rules
- Run the model SQL inside `{% call statement('main') %}`.
- Return `{'relations': [...]}` so dbt updates its relation cache; if you rename or drop other relations, use `adapter.rename_relation` / `adapter.drop_relation` so the cache stays correct.
- Run `pre_hooks` and `post_hooks` with `run_hooks`, and commit the transaction with `adapter.commit()` in the cleanup phase or dbt rolls it back.
- Adapter-specific: use `adapter='<name>'` for an override and `default` for the generic version.
- Study the built-in `table`/`incremental` materializations for your adapter and copy their structure.

## Testing
Run against a dev target: first run (no existing relation), second run (existing relation), `--full-refresh`, and failing SQL.

## Verify
- [ ] `dbt run -s model` twice succeeds and the model appears in the warehouse.
- [ ] Hooks run and the transaction is committed.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt guide on creating materializations: `materialization` block syntax with adapter name or `default` and multiple dispatch, `pre_hooks`/`post_hooks` with `run_hooks`, `statement('main')`, `adapter.commit()` in cleanup, returning `{'relations': [...]}` to update the relation cache, `adapter.drop_relation`/`rename_relation`, static-analysis rules for custom materializations. The skeleton is the documented `my_view` example. Removed unconfirmed claims about swap-based builds, `load_cached_relation`, `make_temp_relation`, grants and docs persistence helpers inside materializations, and a failure-cleanup guarantee.

Method: documentation only; no commands were run.
