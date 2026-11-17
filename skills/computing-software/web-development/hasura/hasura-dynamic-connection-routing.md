---
id: computing-software.web-development.hasura.hasura-dynamic-connection-routing
name: hasura-dynamic-connection-routing
category: computing-software
field: web-development
product: hasura
tags: [hasura, dynamic-routing, kriti, connection-template, multi-tenant, postgres]
level: advanced
status: docs-checked
description: "Route GraphQL requests to different Postgres connections using a Kriti connection_template and connection_set based on role, headers or tenant."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/databases/database-config/dynamic-db-connection.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the database connection per request (per-role credentials, tenant shards, no-stale reads).

Availability: Hasura Cloud and Enterprise, Postgres and Postgres-like backends only.

Only non-admin roles use the connection template; the admin role always uses the primary connection.

Metadata shape from the docs (these keys sit under the source's `configuration`, beside `connection_info`; the `pg_add_source` Metadata API takes the same keys):

```yaml
connection_info:
  database_url:
    from_env: <DATABASE_URL_ENV>
connection_template:
  template: |
    {{ if $.request.session?["x-hasura-role"] == "user" }}
      {{$.primary}}
    {{else}}
      {{$.connection_set.db_1}}
    {{ end }}
connection_set:
  - name: db_1
    connection_info:
      database_url:
        from_env: <OTHER_DB_URL_ENV>
```

The template may resolve to:
- `$.connection_set.<name>` (request fails if the name is not defined),
- `$.primary`,
- `$.read_replicas` (fails for mutations),
- `$.default` (normal behaviour: replicas for reads if configured, primary for mutations).

Context available under `$.request`: `headers` (names in lowercase), `session` (the `x-hasura-*` session variables) and `query` (`operation_type`, plus optional `operation_name`).

Steps: Console: `Dynamic Routing` tab of the Edit Data Source page (pick a template or Custom Template, Add Connection, then `Update Connection Template`). Or put the config in the databases metadata file and run `hasura metadata apply`.

Testing: the Console `Validate` button on the Dynamic Routing tab, or the `pg_test_connection_template` Metadata API with `source_name` and a `request_context`; it returns `routing_to` and `value`. A `connection_template` passed in the API call takes precedence over the source's.

Gotchas (Limitations section):
- The GraphQL schema is derived from the primary connection only. Members of `connection_set` must have an identical Postgres schema; Hasura does not check this, and a mismatch can cause runtime exceptions.
- Event Triggers fire only for mutations on the primary connection.
- CLI migrations cannot be applied to a connection set member, and only the primary database can be edited in the Console.

## Checked

2026-11-04. Confirmed against the cited pages: dynamic-db-connection page: availability, how it works, admin uses primary, template outputs, request context, YAML and pg_add_source shape, Console and pg_test_connection_template testing, limitations. Removed or corrected: the claim about subscription multiplexing and the Verify step (not on the page).

Method: documentation only; no commands were run.
