---
id: computing-software.ai-ml-engineering.litellm.litellm-pgbouncer-prepared-statements
name: litellm-pgbouncer-prepared-statements
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, pgbouncer, prepared-statements, database-disable-prepared-statements]
level: advanced
status: docs-checked
description: "Stop Prisma reusing server-side prepared statements behind PgBouncer transaction pooling with database_disable_prepared_statements."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
general_settings:
  database_disable_prepared_statements: true
```

Effect: appends `pgbouncer=true` to the Prisma connection URL, so each query is prepared fresh instead of reusing a cached plan.

Use it when:

- LiteLLM connects to Postgres through PgBouncer in transaction pooling mode, where reused prepared statements break because consecutive queries can land on different server connections.
- You run rolling deployments with schema migrations and see `cached plan must not change result type` errors. These appear when a migration changes the result type of a column referenced by a plan that a pooled connection still holds.

Tradeoff: every query pays the prepare cost, adding a small per-query overhead.

Precedence: an explicit `pgbouncer` key in `database_extra_connection_params` takes precedence over this flag.

Related pool arithmetic: `database_connection_pool_limit` is applied per worker, so with N instances of W workers each, size it as the database maximum connections divided by (N x W), rounded down for a buffer.

```
general_settings:
  database_connection_pool_limit: 10
  database_extra_connection_params:
    pgbouncer: "true"
    statement_cache_size: 0
```

These settings live in the general_settings section, so they are subject to the config-versus-database ownership rule: once declared in config.yaml they cannot be changed from the Admin UI.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/configs (database pool, prepared statements and config-vs-database sections)
