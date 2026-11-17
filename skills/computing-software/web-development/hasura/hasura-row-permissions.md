---
id: computing-software.web-development.hasura.hasura-row-permissions
name: hasura-row-permissions
category: computing-software
field: web-development
product: hasura
tags: [hasura, permissions, row-level, authorization, session-variables]
level: practitioner
status: docs-checked
description: "Restrict which rows a Hasura role can select, insert, update or delete using boolean expressions over columns and X-Hasura session variables."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/row-level-permissions.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/permissions-operators.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make users see and change only their own rows.

A row permission is a boolean expression restricting access to rows for each operation and role. It can use static values, column values (including related tables or nested objects), session variables and operators. Example allowing a user to read only their own record:

```json
{ "id": { "_eq": "X-Hasura-User-Id" } }
```
For select, the expression decides whether a row can be read. For insert, update and delete it decides whether the mutation as a whole is allowed. Update has both a "Pre-update check" and a "Post-update check" (useful when the new data is unknown until changed).

Operators (permissions operators page): `_eq`, `_ne`, `_gt`, `_lt`, `_gte`, `_lte`, `_in`, `_nin`, `_is_null` (all column types except json and jsonb); `_and`, `_or`, `_not`; `_exists`; string operators such as `_like`, `_nlike`, `_ilike`; column comparison operators `_ceq`, `_cne`, `_cgt`, `_clt`, `_cgte`, `_clte`; and JSONB operators.

Set it in the Console under Data -> [table] -> Permissions, or in the table metadata yaml:

```yaml
select_permissions:
  - role: user
    permission:
      columns: [id, name]
      filter:
        id:
          _eq: X-Hasura-User-Id
```
Apply with `hasura metadata apply`, or use the Metadata API (`pg_create_select_permission`).

More patterns on the page: relationships in the filter (`usersInVendorsByVendorId: { user_id: { _eq: X-Hasura-User-Id } }`), `_exists` with `_table` and `_where` for unrelated tables, and remote source relationships (v2.33.0 and onwards, with limitations such as one level deep and no subscriptions).

Array session variables with `_in`, `_nin`, `_has_any_keys` or `_has_all_keys` are supported from v1.0.0-beta.3; the example value is `X-Hasura-Allowed-Ids: {1,2,3}` used as `user_id: { _in: X-Hasura-Allowed-Ids }`.

## Checked
2026-11-07. Read in full both cited pages (row-level-permissions.mdx and permissions-operators.mdx; GitHub file view, no snippet files, only Thumbnail, Tabs and TabItem components).
Confirmed: every statement above against these pages.
Removed: "checks for insert and update are validated against the row after the change" (the page describes pre- and post-update checks instead), the session-variable typing gotcha (not on these pages), and the invented Verify step.
Method: documentation only; no commands were run.
