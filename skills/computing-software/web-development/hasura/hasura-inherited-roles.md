---
id: computing-software.web-development.hasura.hasura-inherited-roles
name: hasura-inherited-roles
category: computing-software
field: web-development
product: hasura
tags: [hasura, authorization, inherited-roles, roles, permissions]
level: advanced
status: docs-checked
description: "Combine permissions of several Hasura roles into an inherited role defined by a role_set, via inherited_roles.yaml or the add_inherited_role API."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/inherited-roles.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give a role the union of other roles' permissions.

Metadata file `metadata/inherited_roles.yaml`:

```yaml
- role_name: sample_inherited_role
  role_set:
    - user
    - editor
```
Or the Metadata API:

```json
{
  "type": "add_inherited_role",
  "args": {
    "role_name": "sample_inherited_role",
    "role_set": ["user", "editor"]
  }
}
```
Console path: `Settings` (gear) tab, `Inherited Roles`; enter the name, Create, pick the role set, then Save Role.

Rules from the docs:
- An inherited role inherits permissions from two or more roles (its role set) and can be used like any other role, for example as `X-Hasura-Role`.
- Cycles are not allowed: for example `inherited_role1` inheriting `inherited_role2` while `inherited_role2` inherits `inherited_role1` will not work.
- A separate explicit permission for an entity and role pair overrides the inherited one.
- Select permissions: the row filters are OR-ed, so with `P1`, `P2` a column from one role is returned when that role's filter holds and is `null` otherwise (a column granted by every role is always accessible, and one granted by none is not). Limit is the maximum of the limits, aggregation is allowed if any role allows it, and scalar computed fields follow the column rule.
- Mutation and Remote Schema permissions are inherited only when the permission is identical in every role of the set; a conflict marks that entity/role metadata inconsistent (visible via `get_inconsistent_metadata`) until you add an explicit permission.
- Actions and custom functions: access if any role in the set has it.

Apply with `hasura metadata apply`.

Gotcha: in the docs' example a column such as `email` comes back `null` for rows where the role that grants it does not match, even though the database value is not null.

## Checked

2026-11-04. Confirmed against the cited pages: inherited-roles page: Console path, YAML and API, cycles, override, select-permission combination rules, mutation conflict handling, actions/functions inheritance. Removed or corrected: the JWT-role claim (not on the page), the vague combination gotcha and the Verify step.

Method: documentation only; no commands were run.
