---
id: computing-software.web-development.hasura.hasura-restified-endpoints
name: hasura-restified-endpoints
category: computing-software
field: web-development
product: hasura
tags: [hasura, rest, restified, openapi, endpoints]
level: practitioner
status: docs-checked
description: "Publish GraphQL operations as REST endpoints in Hasura with RESTified endpoints, route parameters, and export an OpenAPI 3 spec."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/restified/create.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/restified/export-oas.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/restified/restified-config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve REST clients from saved GraphQL operations (Hasura Cloud and EE).

Available for Postgres, MS SQL Server, Citus, AlloyDB and CockroachDB.

Two ways to create: default CRUD-style endpoints from a table (per the Quickstart guide), or a custom one from GraphiQL. For custom: in the API tab of the Console write a query, click the REST button in the Explorer, then enter a name, an optional description, a location such as `product/:id` and an allowed method, and click Create.

Four required fields: Name, Location (appended to the instance base URL; `:var` segments are replaced by argument values), HTTP method (GET, POST, PUT, PATCH or DELETE) and the GraphQL operation (a query or a mutation).

Call it:

```bash
curl 'https://<your-hasura-project>/api/rest/product/<ID>' --header 'x-hasura-admin-secret: <ADMIN_SECRET>'
```
The response body is the query's data object (for example `{"products_by_pk": {...}}`).

Rules from the docs:
- Only queries and mutations are supported, not subscriptions.
- A location with `/products/:manufacturerId` passes `manufacturerId` to the query as a variable.
- Mutations are executed with POST. They can take a JSON body whose keys match the mutation's variable names, which suits mutations with several arguments.
- `@cached` on the query inserts HTTP caching headers into responses.
- The REST endpoints tab (API section) has an Export OpenAPI Spec button that downloads an OpenAPI 3.0 JSON file for all RESTified endpoints for admin roles; an API can also download it.

## Checked
2026-11-07. Read in full all three cited pages (create.mdx, export-oas.mdx, restified-config.mdx; GitHub file view; the GraphiQLIDE sample components render no text, and the export page links to an API page that was not cited or read).
Confirmed: every item above.
Removed: `rest_endpoints.yaml`/query-collection storage claim, "permissions and roles work as with GraphQL", the uniqueness/apply gotcha, the "REST button then generate from a table" Console path, the "path and query parameters" wording (only path arguments are shown), and the invented Verify step.
Method: documentation only; no commands were run.
