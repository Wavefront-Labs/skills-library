---
id: computing-software.web-development.strapi.database-config-file
name: database-config-file
category: computing-software
field: web-development
product: strapi
tags: [strapi, config-database, postgres, mysql, sqlite, knex, ssl]
level: practitioner
status: docs-checked
description: "config/database: client values, connection parameters, a PostgreSQL example with env(), SSL notes, and unsupported databases."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/database.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config/database

Supported: SQLite, MySQL, MariaDB, PostgreSQL. MongoDB and other NoSQL are not supported. Do not connect to a database not created by a Strapi app, or to a Strapi v3 database.

The file has `connection` (Knex options) and `settings` (Strapi settings). `client` values are rewritten to packages: `sqlite` to better-sqlite3, `mysql` to mysql2, `postgres` to pg.

Connection parameters: `connectionString` (overrides the others when set), `host`, `port`, `database` (or `filename` for SQLite), `user`, `password`, `timezone` (default `utc`), `schema` (Postgres only), `ssl`.

```js
module.exports = ({ env }) => ({
  connection: {
    client: 'postgres',
    connection: {
      connectionString: env('DATABASE_URL'),
      host: env('DATABASE_HOST', '127.0.0.1'),
      port: env.int('DATABASE_PORT', 5432),
      database: env('DATABASE_NAME', 'strapi'),
      user: env('DATABASE_USERNAME', 'strapi'),
      password: env('DATABASE_PASSWORD', 'strapi'),
      schema: env('DATABASE_SCHEMA', 'public'), // Not required
      ssl: env.bool('DATABASE_SSL', false) && {
        rejectUnauthorized: env.bool('DATABASE_SSL_SELF', false), // For self-signed certificates
      },
    },
    pool: { min: env.int('DATABASE_POOL_MIN', 2), max: env.int('DATABASE_POOL_MAX', 10) },
    debug: false,
  },
});
```

The page warns of an SSL issue: to disable SSL set `ssl` to a boolean (e.g. `ssl: env('DATABASE_SSL', false)`). Client-side CA verification needs the `ssl` object with the CA converted to a string via `fs`.

## Checked

2026-11-04: checked against the Strapi docs page Database configuration (configurations/database). Confirmed: supported databases and the unsupported-database warning, `connection` and `settings` objects, client rewrites (better-sqlite3, mysql2, pg), connection parameters including `connectionString` override, `timezone` default `utc` and Postgres-only `schema`, the PostgreSQL example, the SSL caution and CA example. Removed: nothing.

Method: documentation only; no commands were run.
