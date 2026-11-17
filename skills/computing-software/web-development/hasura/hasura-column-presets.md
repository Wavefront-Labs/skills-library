---
id: computing-software.web-development.hasura.hasura-column-presets
name: hasura-column-presets
category: computing-software
field: web-development
product: hasura
tags: [hasura, permissions, column-presets, session-variables, insert]
level: practitioner
status: docs-checked
description: "Set insert or update column values automatically from session variables with Hasura column presets, removing the field from that role's schema."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/column-presets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make the server fill columns such as the owner id, so clients cannot forge them.

Column presets are set in a role's insert or update permission. Defining a preset removes the ability to insert or update that column manually for the role, and the field is removed from the role's generated GraphQL schema.

Metadata example:

```yaml
insert_permissions:
  - role: user
    permission:
      check: {}
      set:
        user_id: x-hasura-User-Id
      columns: [title, body]
```
Apply with `hasura metadata apply` (file `metadata/databases/[database-name]/tables/[table-name].yaml`). Console: Data -> [table] -> Permissions -> insert / update. Values can be session variables or static data. Via the Metadata API, use `pg_create_insert_permission` with a `set` map (or the update permission).

Gotcha: because the field is removed from the role's schema, clients must stop sending that column.

## Checked

2026-11-04. Confirmed against the cited pages: column-presets page: removal from schema, Console path, YAML `set`, pg_create_insert_permission example, session variable or static data. Removed or corrected: the invented row-permission pairing, the Column presets menu label, and the Verify step.

Method: documentation only; no commands were run.
