---
id: computing-software.web-development.hasura.hasura-connect-database-env-var
name: hasura-connect-database-env-var
category: computing-software
field: web-development
product: hasura
tags: [hasura, database, postgres, metadata, connection-string]
level: intro
status: docs-checked
description: "Connect a Postgres or Postgres-compatible database to Hasura using an environment variable in metadata, the Console, or the pg_add_source API."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/databases/quickstart.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/databases/postgres/index.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/graphql-engine-flags/reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: attach a data source so Hasura generates a GraphQL API from its schema.

Steps:
1. Put the connection string in an env var (for example PG_DATABASE_URL). The docs recommend env vars over a raw string because a raw string is exposed as part of the Hasura metadata, and env vars make staging and production setups easy to vary.
2. In the Console go to `Data -> Manage -> Connect Database`, or declare the source in `metadata/databases/databases.yaml`:

```yaml
- name: <db-name>
  kind: postgres
  configuration:
    connection_info:
      database_url:
        from_env: PG_DATABASE_URL
```
3. Run `hasura metadata apply`, or call the Metadata API type `pg_add_source` with `configuration.connection_info.database_url.from_env`.

Notes from the docs:
- From v2.0.0 databases can be connected and removed without restarting the engine.
- `HASURA_GRAPHQL_DATABASE_URL` (flag `--database-url`) is a Postgres connection string that Hasura adds to the connected data sources automatically; `HASURA_GRAPHQL_METADATA_DATABASE_URL` selects the database used to store Hasura's metadata.
- The Postgres page lists AlloyDB, AWS RDS Aurora, Neon, Supabase, Timescale and Yugabyte among others.
- Hasura Cloud does not host databases; it connects to third-party ones.

Gotcha: connection details set as a plain string are exposed as part of the Hasura metadata, which is why the docs recommend env vars.

## Checked

2026-11-04. Confirmed against the cited pages: databases quickstart, Postgres index and flags reference: env-var recommendation, Console path, databases.yaml and pg_add_source `from_env`, v2.0.0 dynamic connect, DATABASE_URL and METADATA_DATABASE_URL, Cloud not hosting databases. Removed or corrected: the Console-typed-string metadata wording (reworded to the page's) and the Verify step.

Method: documentation only; no commands were run.
