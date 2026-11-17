---
id: computing-software.web-development.hasura.hasura-read-replicas
name: hasura-read-replicas
category: computing-software
field: web-development
product: hasura
tags: [hasura, read-replicas, postgres, scaling, metadata]
level: practitioner
status: docs-checked
description: "Route queries and subscriptions to Postgres read replicas in Hasura Cloud or Enterprise while mutations and metadata calls stay on the primary."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/databases/database-config/read-replicas.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: offload read traffic to replicas.

How it works per the docs: Hasura Cloud and Enterprise route queries and subscriptions across read replicas and send all mutations and Metadata API calls to the primary. A replica is selected at random with a uniform distribution; Hasura does no other load balancing.

Steps (Postgres):
1. Console: Data -> Manage -> [database] -> Edit, or add the config to the metadata databases file (the page writes the path as `/metadata/databases/database.yaml`):

```yaml
- name: <db-name>
  kind: postgres
  configuration:
    connection_info:
      database_url:
        from_env: <DATABASE_URL_ENV>
      pool_settings:
        idle_timeout: 180
        max_connections: 50
        retries: 1
    read_replicas:
      - database_url:
          from_env: <DATABASE_REPLICA_URL_ENV>
        pool_settings:
          idle_timeout: 180
          max_connections: 50
          retries: 1
```
2. Run `hasura metadata apply`.
3. Alternatively call the `pg_add_source` Metadata API with `"replace_configuration": true` and a `read_replicas` array under `configuration` (each with `database_url` and `pool_settings`).

MS SQL Server uses the same shape with `kind: mssql`, `connection_string` instead of `database_url`, and the `mssql_add_source` API.

Only for v1.3 projects: `HASURA_GRAPHQL_READ_REPLICA_URLS` (comma-separated), `HASURA_GRAPHQL_CONNECTIONS_PER_READ_REPLICA` and `HASURA_GRAPHQL_STRIPES_PER_READ_REPLICA`. These are no longer supported in v2.0 and above.

## Checked
2026-11-07. Read in full the single cited page (read-replicas.mdx; GitHub file view, no snippet files).
Confirmed: routing behaviour, yaml, API calls, v1.3 variables.
Removed: the replication-lag gotcha and the dynamic-connection-routing claim (not on this page), the invented Verify step. Corrected the v1.3 note (the page says the env vars are unsupported from v2.0) and the yaml (pool_settings under connection_info as on the page).
Method: documentation only; no commands were run.
