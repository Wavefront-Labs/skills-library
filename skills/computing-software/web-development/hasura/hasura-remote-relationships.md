---
id: computing-software.web-development.hasura.hasura-remote-relationships
name: hasura-remote-relationships
category: computing-software
field: web-development
product: hasura
tags: [hasura, remote-relationships, remote-schemas, joins, cross-database]
level: advanced
status: docs-checked
description: "Join Hasura data to remote schemas or other databases with remote relationships, mapping local columns or static values to remote arguments."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/remote-relationships/remote-schema-relationships.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/remote-relationships/remote-schema-db-relationships.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/remote-relationships/remote-source-relationships.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query across sources as if they were one graph. Hasura still handles security and authorization for the joins.

Types covered by these pages:
- Remote schema to remote schema (v2.6.0 and above): inputs for the second schema's field come from a From column or a From static value.
- Remote schema to database (v2.6.0 and above): same idea, joining a remote schema type to a table.
- Database to remote database (Postgres, v2.1.0 and above): object (many-to-one) or array (one-to-many), defined on the source-side table.

Remote schema to remote schema, in `remote_schemas.yaml` (`to_remote_schema` with `remote_schema`, `lhs_fields` and a `remote_field` whose arguments use `$user_id`) or the `create_remote_schema_remote_relationship` and `update_remote_schema_remote_relationship` APIs. The page's yaml sample is not valid as printed (a list item under `relationships`), so build from the API payload:

```json
{ "type": "create_remote_schema_remote_relationship",
  "args": { "name": "user", "remote_schema": "order-remote-schema", "type_name": "Order",
    "definition": { "to_remote_schema": { "remote_schema": "user-remote-schema",
      "lhs_fields": ["user_id"],
      "remote_field": { "user": { "arguments": { "id": "$user_id" } } } } } } }
```
Remote schema to database uses the same API with a `to_source` definition: `relationship_type` (object), `source`, `table` and `field_mapping` (for example `user_id: id`). Console: Remote Schema -> [name] -> Relationships tab -> Add a new relationship.

Database to remote database: fields are Relationship type, Name, Reference Source, Reference Table and Field Mapping. In `metadata/databases/<db>/tables/<table>.yaml`:

```yaml
remote_relationships:
  - name: user
    definition:
      to_source:
        relationship_type: object
        source: pg2
        table: {name: user, schema: public}
        field_mapping:
          user_id: id
```
Or the `pg_create_remote_relationship` / `pg_update_remote_relationship` APIs with `to_source`. Console: Data > [database] > [table] > Relationships > Add Relationships. Then `hasura metadata apply`. Test in GraphiQL, for example `query { order { id user_id user { id name } } }`.

## Checked
2026-11-07. Read in full all three cited pages (GitHub file view; GraphiQLIDE sample components render no text).
Confirmed: versions, field lists, yaml and API shapes above.
Removed: the "database to remote schema" type (no cited page covers it), "choose a Reference Source ... Reference Table" console path wording for schemas, `remote_field`/`to_source` generic mapping claim, the per-parent-row many-calls gotcha (not stated), the invented Verify step and the made-up users/orders example. Noted that the remote-schema yaml sample on the page is malformed.
Method: documentation only; no commands were run.
