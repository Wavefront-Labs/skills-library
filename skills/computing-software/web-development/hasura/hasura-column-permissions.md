---
id: computing-software.web-development.hasura.hasura-column-permissions
name: hasura-column-permissions
category: computing-software
field: web-development
product: hasura
tags: [hasura, permissions, column-level, authorization, roles]
level: intro
status: docs-checked
description: "Limit which columns a Hasura role may read or write by listing allowed columns inside its select, insert or update permission."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/column-level-permissions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: hide sensitive columns from specific roles.

Column permissions determine which columns are accessible in the rows that are accessible. They are the `columns` list inside a role's permission for an operation (insert, select or update).

Metadata example:

```yaml
select_permissions:
  - role: user
    permission:
      columns: [id, name, email]
      filter: {}
```
Apply with `hasura metadata apply`. Console path: Data -> [table] -> Permissions -> insert / select / update. Metadata API: `pg_create_select_permission` with a `columns` array in the permission (the page's example gives `user` partial access to the columns of accessible rows for select).

Note: the permission pairs `columns` with a row `filter`, so a role sees only the right rows and only the right columns.

## Checked

2026-11-04. Confirmed against the cited pages: column-level-permissions page: definition, Console path, metadata YAML, pg_create_select_permission example. Removed or corrected: claims about the per-role schema, validation-error behaviour, computed-field grants, roles coming into existence and the Verify step (none on the cited page).

Method: documentation only; no commands were run.
