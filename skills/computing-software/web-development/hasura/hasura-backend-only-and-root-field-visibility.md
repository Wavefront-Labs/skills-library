---
id: computing-software.web-development.hasura.hasura-backend-only-and-root-field-visibility
name: hasura-backend-only-and-root-field-visibility
category: computing-software
field: web-development
product: hasura
tags: [hasura, permissions, backend-only, root-fields, query-root-fields]
level: advanced
status: docs-checked
description: "Restrict mutations to trusted backends with backend_only and hide chosen root fields per role using query_root_fields and subscription_root_fields."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/backend-only.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/disabling-root-fields.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tighten which entry points a role sees.

Backend-only: set `backend_only: true` inside an insert, update or delete permission (Console: `Data -> [table] -> Permissions -> [role] -> insert / update / delete -> Backend only`; update and delete need v2.8.0+). The mutation is hidden from the public-facing schema and becomes visible only when the request carries `x-hasura-admin-secret` (if authorization is configured), `x-hasura-use-backend-only-permissions: true` and `x-hasura-role`.

```yaml
insert_permissions:
  - role: user
    permission:
      check: {}
      columns: [title]
      backend_only: true
```
Root field visibility (from v2.8.0): in a select permission, list which root fields the role may use (Console: select permission, Root fields permissions).

```yaml
select_permissions:
  - role: user
    permission:
      columns: [id, name]
      filter: {}
      query_root_fields: [select_by_pk]
      subscription_root_fields: [select_by_pk, select_stream]
```
By default query roots are `select`, `select_by_pk`, `select_aggregate`; subscriptions add `select_stream`. `null` or an omitted list allows all root fields; an empty array allows none.

Use case: with no root fields enabled, a table is reachable only through a relationship from another table the role can access.

## Checked

2026-11-04. Confirmed against the cited pages: backend-only and disabling-root-fields pages: supported mutations, v2.8.0, required headers, Console paths, root field names, null versus empty array, relationship-only use case. Removed or corrected: the claim that Action handlers count as trusted backends, the claimed relationship gotcha wording and the Verify step.

Method: documentation only; no commands were run.
