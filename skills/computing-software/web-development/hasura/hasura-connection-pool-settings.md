---
id: computing-software.web-development.hasura.hasura-connection-pool-settings
name: hasura-connection-pool-settings
category: computing-software
field: web-development
product: hasura
tags: [hasura, connection-pool, postgres, mssql, performance, pool-settings]
level: practitioner
status: docs-checked
description: "Tune Hasura connection pooling with total_max_connections on Cloud or max_connections when self-hosted, for Postgres and MS SQL Server sources."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/databases/database-config/cloud-connection-pooling.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/production-checklist.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size the database connection pool so Hasura stays within database limits under load.

Facts from the docs:
- Pooling is always on, and is available only for Postgres and MS SQL Server sources.
- Hasura Cloud uses an elastic pool that grows and shrinks with usage and respects a configured maximum. Set `total_max_connections`; if both it and `max_connections` are set, `total_max_connections` wins. The limit is best effort, so keep it slightly below the database's true maximum.
- In self-hosted deployments the setting is `max_connections` and it is per server instance, so the total across a project is number of server instances multiplied by `max_connections`.
- Other pool settings named in the docs: `idle_timeout` (idle connections are released after it), `connection_lifetime`, `pool_timeout` (times out requests blocked on a saturated pool) and `retries`.

Steps:
1. Console: Data > Databases > Manage > [database-name] > Edit, then the Connection Settings section (when adding a database, set Total Max Connections for primary and read replica pools).
2. Or in the source's entry in the metadata `databases.yaml`, under `configuration.connection_info`:

```yaml
pool_settings:
  total_max_connections: 60
```
3. Apply with `hasura metadata apply`.

Gotcha: self-hosted `max_connections` applies per server instance, so keep instances times `max_connections` below the database connection limit. The production checklist says to set an appropriate value for Postgres and MS SQL Server databases.

## Checked

2026-11-04. Confirmed against the cited pages: cloud-connection-pooling and production-checklist pages: always-on pooling, source support, elastic pool, total_max_connections vs max_connections, per-instance multiplication, Console path, YAML placement, other pool setting names. Removed or corrected: the self-hosted YAML sample with max_connections and idle_timeout values (replaced with the page's YAML), `retries` value claim and the Verify step.

Method: documentation only; no commands were run.
