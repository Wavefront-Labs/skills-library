---
id: computing-software.data-engineering.dbt.analyses-folder
name: analyses-folder
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-analyses, analyses, compiled-sql, ad-hoc-queries]
level: intro
status: docs-checked
description: "Use the dbt analyses folder for version-controlled ad-hoc and audit SQL that uses ref and Jinja but is compiled, never materialized, and how to run its output."
sources:
  - https://docs.getdbt.com/docs/build/analyses
  - https://docs.getdbt.com/reference/project-configs/analysis-paths
  - https://docs.getdbt.com/reference/commands/show
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analyses folder

**Goal:** keep useful one-off SQL (audits, reconciliation queries, migration checks) in the repo with `ref()` resolution, without creating warehouse objects.

## How it works
- `.sql` files in the directories listed in `analysis-paths` in `dbt_project.yml` (`dbt init` sets it to `analyses`) are compiled but not executed. Without the setting, dbt compiles no `.sql` files as analyses.
- They can use `ref()`, so the SQL selects from models in an environment-agnostic way.

```sql
-- analyses/audit_orders_vs_legacy.sql
select count(*) as new_rows from {{ ref('fct_orders') }}
union all
select count(*) from {{ ref('fct_orders_legacy') }}
```

## Run it
```bash
dbt compile --select audit_orders_vs_legacy
# then run the compiled SQL in a SQL client
dbt show --select audit_orders_vs_legacy    # previews the first 5 rows by default; --limit n changes it
```

## Properties
```yaml
version: 2
analyses:
  - name: audit_orders_vs_legacy
    description: Row-count reconciliation used during the warehouse migration.
```



## Gotchas
- Analyses are compiled, not executed or materialized, so nothing in production should depend on them.
- `dbt show` can preview an analysis, and `dbt show --inline` runs ad-hoc SQL, so use a read-only profile or role when previewing.

## Verify
`dbt compile` produces the compiled SQL with `ref()` resolved for the current target.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: Analyses are compiled but not executed; `ref()` is allowed; `analysis-paths` default and `dbt init` value; analysis properties file with `analyses:` and `description`; `dbt show` previews analyses (default 5 rows, `--limit`, `--inline` caveat). Removed unconfirmed claims about build-time compilation, compiled output paths, DAG/docs visibility, `adapter.get_relation` use and third-party audit helpers.

Method: documentation only; no commands were run.
