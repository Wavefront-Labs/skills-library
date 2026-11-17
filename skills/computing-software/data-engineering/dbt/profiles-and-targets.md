---
id: computing-software.data-engineering.dbt.profiles-and-targets
name: profiles-and-targets
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, profiles-yml, dbt-targets, target-name, dbt-profiles-dir, threads, dbt-debug, connection-config, service-account]
level: practitioner
status: gated
description: "Configure dbt connections: profiles.yml outputs per target (dev/ci/prod), env_var for secrets, DBT_PROFILES_DIR and --target, threads, per-adapter auth, and dbt debug."
sources:
  - https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles
  - https://docs.getdbt.com/reference/dbt-jinja-functions/target
  - https://docs.getdbt.com/reference/commands/debug
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# profiles.yml and targets

**Goal:** the same project runs against dev, CI and prod warehouses by switching a target, with no secrets in git.

## profiles.yml
```yaml
acme:                           # must equal `profile:` in dbt_project.yml
  target: dev                   # default target
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      authenticator: externalbrowser            # SSO for humans (gated: unconfirmed, source is paywalled or blocked)
      role: transformer_dev
      warehouse: transforming_xs
      database: analytics_dev
      schema: "dbt_{{ env_var('USER') | lower }}"   # personal dev schema
      threads: 8
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: svc_dbt_prod
      private_key_path: "{{ env_var('SNOWFLAKE_PRIVATE_KEY_PATH') }}"   # key-pair for service users (gated: unconfirmed, source is paywalled or blocked)
      role: transformer_prod
      warehouse: transforming_m
      database: analytics
      schema: analytics
      threads: 16
```
Other adapters: BigQuery (`method: oauth` / `service-account` + `keyfile`), Databricks (`host`, `http_path`, `token` or OAuth), Postgres/Redshift (`host`, `user`, `password`, `dbname`) (gated: unconfirmed, source is paywalled or blocked). The Snowflake keys above were not run (no account); the profile mechanics (targets, `--target`, search order) were run with dbt-duckdb.

## Selecting
```bash
dbt run --target prod
export DBT_PROFILES_DIR=/etc/dbt          # where profiles.yml lives (default ~/.dbt)
dbt run --profiles-dir ./ci               # per-command
dbt debug --target prod                   # validates profile, connection, and project
```
Search order, checked with `dbt debug --config-dir` on 1.12.6: `--profiles-dir` > `DBT_PROFILES_DIR` > current working directory > `~/.dbt/`. A stray `profiles.yml` in the repo root therefore wins over `~/.dbt`; being explicit in CI avoids surprises.

## Using target in code
```sql
{% if target.name == 'prod' %} ... {% endif %}
{{ config(materialized = 'table' if target.name == 'prod' else 'view') }}
```
Use sparingly; environment-dependent logic makes dev results differ from prod.

## Threads
`threads` = concurrent model builds. Start at 4-8 for dev, 8-32 for prod depending on warehouse concurrency limits (Snowflake queues beyond warehouse capacity; BigQuery has slot limits).

## Gotchas
- `env_var('X')` with no default fails parse if X is unset; give defaults only for non-secrets: `env_var('DBT_THREADS', '8') | int`.
- Secrets used via `env_var` must be prefixed `DBT_ENV_SECRET_` to be scrubbed from logs (docs: replaced with `*****`).
- dbt Cloud does not use profiles.yml; connections are configured per environment in the UI/API (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `dbt debug --target <each>` passes in its environment.
- [ ] `git grep -i password` finds no credentials.
