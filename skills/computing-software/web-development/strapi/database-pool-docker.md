---
id: computing-software.web-development.strapi.database-pool-docker
name: database-pool-docker
category: computing-software
field: web-development
product: strapi
tags: [strapi, database, pool, tarn, docker, acquireconnectiontimeout]
level: advanced
status: docs-checked
description: "Strapi database pooling (Tarn.js via Knex): pool min/max, why min must be 0 in Docker, and the acquire timeout."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/database.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database pooling

`connection.pool` in `config/database` passes Tarn.js options (used by Knex.js). Example from the page:

```js
pool: { min: env.int('DATABASE_POOL_MIN', 2), max: env.int('DATABASE_POOL_MAX', 10) },
```

## Docker trap
When using Docker, change the pool `min` to `0`: Docker kills idle connections, making it impossible to keep any open connections to the database.

```js
pool: { min: 0, max: env.int('DATABASE_POOL_MAX', 10) },
```

## Related
- `acquireConnectionTimeout` (default `60000` ms): how long Knex waits before throwing a timeout when acquiring a connection.
- `debug` (default `false`): show database exchanges and errors.
- `useNullAsDefault` is SQLite only, default `true`.

## Pool parameters (Strapi page defaults)
- `min` `2`, `max` `10`
- `acquireTimeoutMillis` `60000`, `createTimeoutMillis` `30000`, `destroyTimeoutMillis` `5000`
- `idleTimeoutMillis` `30000`, `reapIntervalMillis` `1000`, `createRetryIntervalMillis` `200`
- `afterCreate`: callback run when the pool acquires a new connection.

When a connection cannot be acquired before `acquireConnectionTimeout` or `pool.acquireTimeoutMillis` (whichever is smaller), Knex throws a `KnexTimeoutError`. Strapi adds `error.details` with pool state unless `settings.poolTimeoutDiagnostics` is `false`.

## Checked

2026-11-04: checked against the Strapi docs page Database configuration (configurations/database). Confirmed: Tarn.js options through `connection.pool`, the example, the Docker `min: 0` caution, `acquireConnectionTimeout` default 60000, `debug` default false, `useNullAsDefault` SQLite-only default true. Replaced: the pointer to external docs with the full pool parameter list and defaults from the page, plus the timeout diagnostics behaviour.

Method: documentation only; no commands were run.
