---
id: computing-software.web-development.hasura.hasura-remote-schema-permissions
name: hasura-remote-schema-permissions
category: computing-software
field: web-development
product: hasura
tags: [hasura, remote-schemas, permissions, enable-remote-schema-permissions, argument-presets]
level: advanced
status: docs-checked
description: "Expose only part of a remote schema per role in Hasura by enabling remote schema permissions and presetting arguments, plus auth forwarding patterns."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/auth/remote-schema-permissions.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/auth/remote-schema-forward-auth.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/auth/remote-schema-bypass-auth.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control which remote fields each role can reach (v2.0.0 and above).

Not enabled by default. Start the engine with `--enable-remote-schema-permissions` or `HASURA_GRAPHQL_ENABLE_REMOTE_SCHEMA_PERMISSIONS=true`. Until then all roles have unrestricted access to remote schemas; once on, every role except admin is restricted unless it is granted permissions on the schema's fields.

Role-based schema: give each role a restricted schema in GraphQL IDL. Objects, interfaces and input objects can omit fields; unions can drop possible types; enums can omit values; scalars cannot be changed; field arguments can be a subset. Set it with Remote Schemas -> [name] -> Permissions tab -> pick or enter a role -> select fields and presets -> Save Permissions, in `remote_schemas.yaml` under `permissions` (`role` and `definition.schema`), or with `add_remote_schema_permissions`:

```json
{ "type": "add_remote_schema_permissions",
  "args": { "remote_schema": "countries", "role": "user",
    "definition": { "schema": "schema { query: Query } type Country { name: String! } type Query { continent(code: ID!): Continent }" },
    "comment": "remote schema permissions for role: user" } }
```
(The `schema` string must define every type it references.)

Argument presets constrain inputs with the `@preset` directive on an argument or input object field. Preset arguments are removed from the exposed schema and injected at execution:

```graphql
type Query {
  get_user(id: ID! @preset(value: "x-hasura-user-id")): User
  get_user_activities(user_id: ID!, limit: Int! @preset(value: 10)): [Activity]
}
```
A preset string in `x-hasura-*` form is treated as a session variable; add `static: true` to treat it literally. Input object field presets merge with the user-supplied fields.

Auth forwarding:
- Hasura forwards resolved `x-hasura-*` values as headers to the remote schema; you can also set static headers or forward all client headers. Precedence: configuration headers, then resolved x-hasura-* variables, then client headers.
- Client `x-hasura-*` headers are respected only if `x-hasura-admin-secret` is sent.
- `Set-Cookie` from the remote server reaches the client over HTTP but not WebSocket.
- Bypassing Hasura auth has no first-class option. Workaround for webhook auth: the webhook returns 200 with `x-hasura-role: anonymous` instead of 401, and the remote schema uses Forward all headers from client. For JWT: the auth server issues a static anonymous JWT and the remote server checks the role claim itself.

## Checked
2026-11-07. Read in full all three cited pages (GitHub file view, no snippet files).
Confirmed: every item above. The page's own sample SDL has formatting errors (missing colons), so the examples here are rewritten, not copied.
Removed: the "only part read in depth" gotcha, the invented Verify step, and the vague "or configure a header" forwarding line (replaced by the page's precedence rules). Added `static: true`, input object presets, the flag form, Set-Cookie and JWT bypass notes.
Method: documentation only; no commands were run.
