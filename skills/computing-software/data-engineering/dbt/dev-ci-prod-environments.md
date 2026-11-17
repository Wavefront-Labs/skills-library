---
id: computing-software.data-engineering.dbt.dev-ci-prod-environments
name: dev-ci-prod-environments
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-deployment, dbt-environments, dev-schemas, ci-schema, prod-deployment, environment-isolation, roles-and-warehouses, dbt-cloud-environments, write-audit-publish]
level: advanced
status: docs-checked
description: "Set up dbt environments: personal dev schemas, ephemeral CI schemas, prod with a service identity, separate roles/warehouses, sampling dev data, and write-audit-publish for prod."
sources:
  - https://docs.getdbt.com/docs/environments-in-dbt
  - https://docs.getdbt.com/docs/deploy/deploy-environments
  - https://docs.getdbt.com/docs/build/custom-schemas
  - https://docs.getdbt.com/best-practices/best-practice-workflows
  - https://docs.getdbt.com/docs/build/sample-flag
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dev / CI / prod environments

**Goal:** developers and CI can build freely without touching production objects, and prod builds are reproducible from main.

## Layout
| Env | Who runs | Writes to | Reads | Identity |
|---|---|---|---|---|
| dev | Each developer | A target schema per user (for example `dbt_alice`) | Raw sources (or sampled/cloned) | Personal credentials |
| CI | PR pipeline | A temporary schema unique to the PR (dbt platform: `dbt_cloud_pr_<job_id>_<pr_id>`) | Prod via defer | CI credentials |
| prod | Scheduler on main | Prod schemas | Raw sources | Production credentials |

## Mechanics
- dbt Core: targets in `profiles.yml`; dbt platform: development and deployment environments. The docs recommend different schemas within one warehouse, with the schema and user credentials differing per target.
- `generate_schema_name` decides the schema: by default the custom schema is appended to the target schema (`<target_schema>_<custom_schema>`); a common override uses the custom schema as-is in production (when `target.name == 'prod'`) and prefixes it elsewhere.

## Keeping dev cheap
- Limit data in dev: `{% if target.name == 'dev' %} where created_at >= dateadd('day', -3, current_date) {% endif %}` in staging models (the dbt best-practices example).
- `--defer --state prod-state --favor-state` resolves unselected refs to the production manifest even if the object exists in the dev schema.
- `dbt clone` copies production relations into the dev schema on warehouses with zero-copy cloning.
- `--sample` mode builds models from a time-based sample of data (for example `dbt run --select stg_customers --sample="3 days"`); `--empty` validates without data.

## Prod safety: build, test, then promote
The `dbt clone` docs list blue/green continuous deployment as a use case on warehouses with zero-copy cloning: build and test in a separate schema, then promote. Design the swap or clone step for your warehouse.

## Gotchas
- Keep `target.name` logic in models limited to sampling and naming, so dev exercises the same logic as prod.
- Each user has their own development target schema, so developers do not overwrite each other.

## Verify
- [ ] Prod job runs from the main branch; custom environment variables prefixed `DBT_ENV_CUSTOM_ENV_` are recorded in dbt artifacts and logs.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt environments, custom schemas, local environments, best-practice-workflows, sample flag, clone and env_var docs: dev/ci/prod target names, per-user development schemas (`dbt_alice` example), `generate_schema_name` behaviour and the production-uses-custom-schema pattern with target name `prod`, the dev data limiting example, `--defer --favor-state`, `dbt clone` blue/green use case, `--sample` time-based sampling, `DBT_ENV_CUSTOM_ENV_` prefix, dbt platform CI schema prefix `dbt_cloud_pr_`. Removed unconfirmed warehouse role, compute sizing, Snowflake database swap and `limit_data_in_dev` macro claims.

Method: documentation only; no commands were run.
