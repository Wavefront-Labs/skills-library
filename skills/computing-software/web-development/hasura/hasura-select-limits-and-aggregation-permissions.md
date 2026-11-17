---
id: computing-software.web-development.hasura.hasura-select-limits-and-aggregation-permissions
name: hasura-select-limits-and-aggregation-permissions
category: computing-software
field: web-development
product: hasura
tags: [hasura, permissions, row-limit, aggregation, allow-aggregations]
level: practitioner
status: docs-checked
description: "Cap rows returned per role with a select permission limit and control access to _aggregate fields with allow_aggregations in Hasura."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/row-fetch-limit.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/permissions/aggregation-permissions.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/production-checklist.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect the database from huge result sets and unwanted aggregates.

Row fetch limit, set in the role's select permission:

```yaml
select_permissions:
  - role: user
    permission:
      columns: [id, name]
      filter:
        user_id:
          _eq: X-Hasura-User-Id
      limit: 1
```
The limit restricts the number of rows returned in a response on select operations. The production checklist recommends limiting the rows accessible in one request, to avoid someone querying the entire table in one shot and loading Postgres. The same setting can be made through the `pg_create_select_permission` Metadata API (`"limit": 1` in the permission) and applied from metadata with `hasura metadata apply`.

Aggregation permissions:

```yaml
select_permissions:
  - role: user
    permission:
      columns: [id, name]
      allow_aggregations: true
```
`allow_aggregations: true` enables aggregation queries for the role on select operations.

Console: Data -> [table] -> Permissions -> select -> Row select permissions -> "Limit number of rows", and Aggregation queries permissions (checkbox).

## Checked
2026-11-07. Read in full all three cited pages (row-fetch-limit.mdx, aggregation-permissions.mdx, production-checklist.mdx; GitHub file view, no snippet files, only Thumbnail, Tabs and TabItem components).
Confirmed: the two yaml shapes, the Console paths, the Metadata API field names, the checklist rationale for limits.
Removed: the claim that `<table>_aggregate` root fields and nested aggregates are absent from the schema without `allow_aggregations` (the page says only that it enables aggregation queries), the "silently gets fewer rows / document the limit" gotcha, the console label "Allow role to make aggregation queries" (the page says "Aggregation queries permissions"), and the invented Verify step.
Method: documentation only; no commands were run.
