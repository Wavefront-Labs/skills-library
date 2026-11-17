---
id: computing-software.data-engineering.dbt.vars-and-env-vars
name: vars-and-env-vars
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-vars, env-var, var-function, dbt-env-secret, project-variables, cli-vars, parameterised-runs]
level: practitioner
status: verified
description: "Parameterise dbt runs: var() with defaults in dbt_project.yml, --vars on the CLI, env_var() for environment-specific values, DBT_ENV_SECRET_ scrubbing, and partial-parse effects."
sources:
  - https://docs.getdbt.com/docs/build/project-variables
  - https://docs.getdbt.com/reference/dbt-jinja-functions/env_var
  - https://docs.getdbt.com/reference/dbt-jinja-functions/var
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project vars and env_var

**Goal:** pass run parameters (dates, feature flags, source databases) into models without editing SQL.

## var()
```yaml
# dbt_project.yml
vars:
  start_date: '2024-01-01'
  acme:                          # scoped to this project (packages can have their own)
    lookback_days: 3
```
```sql
where event_date >= '{{ var("start_date") }}'
  and event_date >= dateadd(day, -{{ var("lookback_days") }}, current_date)
```
Override per run:
```bash
dbt run -s fct_events --vars '{"start_date": "2026-10-01", "lookback_days": 10}'
dbt run --vars 'lookback_days: 10'                # YAML string works too
```
`var("x", "default")` supplies an inline default; without one, an undefined var is a compile error ("Required var 'x' not found in config", checked; good: fail loudly).

## env_var()
```sql
from {{ source('raw', 'orders') }}   -- with source database set from env:
```
```yaml
sources:
  - name: raw
    database: "{{ env_var('DBT_RAW_DATABASE', 'raw') }}"
```
- Use for environment-specific values (database names, warehouse sizes) and secrets in profiles.
- `env_var` returns strings: `{{ env_var('DBT_THREADS', '8') | int }}` (checked), `| as_bool` where needed (use capitalised `True`/`False` as the default; lowercase is a string per the docs).
- Prefix secrets `DBT_ENV_SECRET_...`: dbt scrubs their values from logs and allows them only in profiles.yml/packages.yml (model SQL fails to parse: "Secret env vars are allowed only in profiles.yml or packages.yml", checked). Secrets are substituted as plain strings: no filters, no string concatenation, one per config value (dbt docs).
- `DBT_ENV_CUSTOM_ENV_` prefixed vars are recorded with the prefix stripped under `metadata.env` in the artifacts (`run_results.json` showed `{'RUN': 'abc'}`) and are available as `dbt_metadata_envs`, handy for run tags. (`invocation_env` is a different, tracking-only setting.)

## var vs env_var
| Need | Use |
|---|---|
| Per-run parameter chosen by the caller (date range, backfill flag) | `var` + `--vars` |
| Depends on where it runs (dev/prod DB names, credentials) | `env_var` |
| Logic switch by environment | `target.name` (sparingly) |

## Gotchas
- Changing `--vars` between runs disabled partial parsing ("Unable to do partial parsing because config vars ... have changed", checked), so the whole project re-parses; don't rely on vars for high-frequency toggles in huge projects.
- Vars are not visible to `ref()` resolution or selection; you cannot select models by var.
- Quoting: `'{{ var("d") }}'` for dates in SQL; numbers unquoted.

## Verify
- [ ] `dbt compile -s model --vars '...'` shows the intended values in `target/compiled/`.
- [ ] Missing required vars fail at compile, not silently using wrong defaults.
