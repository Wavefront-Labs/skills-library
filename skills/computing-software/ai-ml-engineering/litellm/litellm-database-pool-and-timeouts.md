---
id: computing-software.ai-ml-engineering.litellm.litellm-database-pool-and-timeouts
name: litellm-database-pool-and-timeouts
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, database-connection-pool-limit, prisma, postgres]
level: advanced
status: docs-checked
description: "Size the Prisma connection pool per worker and cap idle or slow Postgres connections with general_settings."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
general_settings:
  database_connection_pool_limit: 10   # default 10, recommended 10-20
  database_connection_timeout: 60
```

The pool limit applies per worker process, not per instance, so each worker creates its own pool.

Formula: `database_connection_pool_limit = MAX_DB_CONNECTIONS / (number_of_instances x number_of_workers_per_instance)`.

Example: a database allowing 100 connections, 1 instance, 8 workers (`--num_workers 8`): 100 / 8 = 12.5, round down to 10 for a safety buffer. Total maximum 80 connections.

Idle connections piling up: use `database_socket_timeout` (the main knob), and `database_connect_timeout` to bound new connections. They map to the Prisma PostgreSQL URL params of the same name minus the prefix, and are appended to both DATABASE_URL and DIRECT_URL. When unset they are omitted and Prisma defaults apply.

```
general_settings:
  database_connection_pool_limit: 20
  database_socket_timeout: 300
  database_connect_timeout: 15
  database_extra_connection_params:
    pgbouncer: "true"
    statement_cache_size: 0
    sslmode: "require"
```

`database_extra_connection_params` is an untyped passthrough: any key you set overrides the LiteLLM-set default for that key (for example pool_timeout). To verify the server certificate against a custom CA such as AWS RDS, set `sslmode: "verify-full"` and `sslrootcert: "/certs/global-bundle.pem"`; LiteLLM translates them into Prisma's sslcert + sslaccept=strict.

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): database_connection_pool_limit (default 10, recommended 10-20), database_connection_timeout, the pool formula and the 100 / 8 = 12.5 example, database_socket_timeout, database_connect_timeout, database_extra_connection_params and the sslmode verify-full translation.

Method: documentation only; no commands were run.
