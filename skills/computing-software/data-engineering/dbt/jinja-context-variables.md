---
id: computing-software.data-engineering.dbt.jinja-context-variables
name: jinja-context-variables
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-context-variables, jinja, target, invocation-id]
level: practitioner
status: docs-checked
description: "Use dbt's Jinja context variables correctly: this, target, invocation_id, run_started_at, flags, execute, model, selected_resources, env_var and modules."
sources:
  - https://docs.getdbt.com/reference/dbt-jinja-functions/this
  - https://docs.getdbt.com/reference/dbt-jinja-functions/run_started_at
  - https://docs.getdbt.com/reference/dbt-jinja-functions/selected_resources
  - https://docs.getdbt.com/reference/dbt-jinja-functions/flags
  - https://docs.getdbt.com/reference/dbt-jinja-functions/execute
  - https://docs.getdbt.com/reference/dbt-jinja-functions/target
  - https://docs.getdbt.com/reference/dbt-jinja-functions/env_var
  - https://docs.getdbt.com/reference/dbt-jinja-functions/modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context variables (this, target, invocation_id, flags)

**Goal:** environment-aware, auditable models and macros using what dbt already exposes.

| Variable | Use |
|---|---|
| `this` | the current model's relation (a Relation); used in incremental filters, e.g. `select max(ts) from {{ this }}`, and in hooks |
| `target.name / schema / type / threads`, `target.database` | active target: name, schema, adapter type, threads; `database` and other fields vary by adapter |
| `invocation_id` | UUID generated for each dbt command; also in `query-comment`, logs, artifacts metadata and BigQuery job labels |
| `run_started_at` | Python `datetime` of when the run started, UTC by default; `{{ run_started_at.strftime("%Y-%m-%d") }}` |
| `flags.FULL_REFRESH`, `flags.EMPTY`, `flags.WHICH` | behave differently on full refresh, `--empty`, or per command (`run`, `test`, ...) |
| `execute` | false while parsing; guard code that needs `run_query` results with it |
| `model` | the graph node for the current model (`model.config`, `model.name`) |
| `selected_resources` | list of unique_ids selected by the command; usable in hooks and `on-run-end`, empty during parsing, not available in `run-operation` |
| `env_var('X', 'default')` | environment config; env vars prefixed `DBT_ENV_SECRET` are allowed only in `profiles.yml` and `packages.yml` and are scrubbed from logs |
| `var('name', default)` | project/CLI vars |
| `modules.datetime`, `modules.pytz`, `modules.re` | Python modules exposed inside Jinja (`modules.itertools` is deprecated since dbt-core 1.10.6) |
| `graph` | project graph for introspective macros; incomplete during parsing |

## Patterns
```sql
select *, '{{ invocation_id }}' as _dbt_invocation_id
from {{ ref('stg_orders') }}
{% if target.name != 'prod' %} where order_date >= dateadd('day', -7, current_date) {% endif %}
```
```sql
{% if execute %}
  {% set max_ts = run_query("select max(updated_at) from " ~ this).columns[0].values()[0] %}
{% endif %}
```

## Gotchas
- Jinja that relies on a database result errors during the parse phase (for example `'None' has no attribute 'table'`), so guard `run_query` with `execute`.
- Secret env vars must start with `DBT_ENV_SECRET`; they cannot be used in `dbt_project.yml` or model SQL, and Jinja filters (including type casts) cannot modify them.
- `run_started_at` is fixed for the whole run; convert time zones with `modules.pytz`.

## Verify
`dbt compile --select <model> --target dev` vs `--target prod` shows the intended differences (compiled SQL is written to `target/compiled/`).

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt Jinja context pages for `this`, `target`, `invocation_id`, `run_started_at`, `selected_resources`, `flags`, `execute`, `model`, `env_var` (secret rules), `modules` and `graph`. Removed unconfirmed claims about env_var values in the manifest, `dbt.current_timestamp()` in the example and an `is_prod()` convention; the `target.name` filter example follows the dbt best-practices workflow.

Method: documentation only; no commands were run.
