---
id: computing-software.web-development.hasura.hasura-computed-fields
name: hasura-computed-fields
category: computing-software
field: web-development
product: hasura
tags: [hasura, postgres, computed-fields, sql-functions, virtual-fields]
level: advanced
status: docs-checked
description: "Add virtual computed fields to Postgres tables from STABLE or IMMUTABLE SQL functions that take the table row, optionally with extra args and session variables."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/computed-fields.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query derived values next to normal columns.

Computed fields run a user-defined SQL function on request. They only exist in the GraphQL API; the database schema is not modified, so the value cannot be fetched as a real column.

Function rules:
- Behavior: only `STABLE` or `IMMUTABLE`.
- Argument modes: only `IN`.
- Exactly one input argument of the table row type (this is the table argument).
- Return type: `SETOF <table-name>` (a table computed field; the return table must be tracked) or a base type (a scalar computed field).
- Extra arguments are allowed and become arguments of the computed field in GraphQL.
- The function does not need to be tracked as a custom function.

Add one via the Console (table `Modify` tab, Computed fields section), metadata (`computed_fields:` block in the table yaml; the example there uses `table_argument: null`), or the Metadata API:

```json
{
  "type": "pg_add_computed_field",
  "args": {
    "table": "authors",
    "source": "default",
    "name": "full_name",
    "definition": {
      "function": "author_full_name",
      "table_argument": "author_row"
    }
  }
}
```
Setting `session_argument` (v1.3.0+) makes Hasura pass session variables as a JSON object with lowercase keys; that argument is not exposed in the GraphQL schema.

Permissions: scalar computed fields are managed like column permissions; table computed fields respect the permissions of the return table. Scalar computed fields whose function takes only the row (and optional session argument) can be used in `where` and `order_by`. In remote relationships only scalar computed fields can be used (v2.0.1+).

## Checked

2026-11-04. Confirmed against the cited pages: computed-fields page: function constraints, no-tracking note, types, Console/CLI/API add flows, session_argument, permissions, filter and remote-relationship limits. Removed or corrected: the loosely worded permissions gotcha and the Verify step.

Method: documentation only; no commands were run.
