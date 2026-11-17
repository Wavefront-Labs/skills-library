---
id: computing-software.data-engineering.dbt.full-refresh-protection
name: full-refresh-protection
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, incremental-models, full-refresh-config, full-refresh, is-incremental, rebuild, protected-models, snapshots]
level: practitioner
status: docs-checked
description: "Control dbt full refreshes: when --full-refresh rebuilds incremental models and seeds, protecting large models with full_refresh: false, and planned rebuilds via a variable."
sources:
  - https://docs.getdbt.com/reference/resource-configs/full_refresh
  - https://docs.getdbt.com/docs/build/incremental-models#how-do-i-rebuild-an-incremental-model
  - https://docs.getdbt.com/reference/commands/seed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full refresh control

**Goal:** nobody accidentally drops and rebuilds a 5-year incremental table whose source history no longer exists, while still allowing planned rebuilds.

## What --full-refresh does
`dbt run --full-refresh` / `dbt build --full-refresh`:
- Incremental models: dbt drops the existing target table and rebuilds it for all time (`is_incremental()` is false).
- Seeds: `--full-refresh` forces a full reload of seed data.

## Protect a model
```yaml
# models/marts/_marts.yml
models:
  - name: fct_events_history
    config:
      full_refresh: false
```
or in SQL `{{ config(full_refresh = false) }}`, or project-level for a folder (`+full_refresh: false`):
```yaml
models:
  my_project:
    marts:
      history:
        +full_refresh: false
```
`full_refresh: true` always performs a full refresh and `false` never does, regardless of `--full-refresh`; `none` or omitted follows the flag. The config applies to models and seeds.

## When to protect
- Models of especially large datasets, which you would never want dbt to fully drop and recreate.

## Planned rebuild of a protected model
1. Override per run: set `full_refresh = var("force_full_refresh", false)` in the config and pass `--vars '{"force_full_refresh": true}'`.

## Schema changes without full refresh
Use `on_schema_change` (`ignore` default, `fail`, `append_new_columns`, `sync_all_columns`) for column changes. None of them backfill old rows for new columns; run manual updates or a `--full-refresh` for that.

## Gotchas
- You cannot override an existing `full_refresh` config from the command line: drive it with a variable as above.

## Verify
- [ ] `dbt run -s fct_events_history --full-refresh` does not drop the protected table.
- [ ] The controlled rebuild path (variable override) is documented in a runbook.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt full_refresh config, incremental models and seed command pages: `--full-refresh` (`-f`) drops and rebuilds incremental models, forces seed reload, the `full_refresh` true/false/none behaviour for models and seeds, recommendation to protect very large datasets, variable override pattern, `on_schema_change` values and the no-backfill note. Removed unconfirmed claims about snapshots, tables and views, cloning before rebuild, CI behaviour and dbt Cloud checkbox precedence.

Method: documentation only; no commands were run.
