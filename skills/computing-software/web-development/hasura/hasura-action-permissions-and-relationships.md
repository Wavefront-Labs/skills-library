---
id: computing-software.web-development.hasura.hasura-action-permissions-and-relationships
name: hasura-action-permissions-and-relationships
category: computing-software
field: web-development
product: hasura
tags: [hasura, actions, permissions, relationships, custom-types]
level: practitioner
status: docs-checked
description: "Restrict Hasura Actions per role with permissions, join action outputs to Postgres tables with relationships, and know the custom type limits."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/action-permissions.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/action-relationships.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/actions/types.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: secure actions and connect their results to the rest of the graph.

Permissions: as with other schema fields, users must be given access to an action. In `metadata/actions.yaml`:

```yaml
actions:
  - name: insertAuthor
    definition:
      kind: synchronous
      handler: <HANDLER_URL>
    permissions:
      - role: user
```
Apply with `hasura metadata apply`. API: `create_action_permission` (args `action`, `role`). Console: `Actions -> [action-name] -> Permissions`, then Save.

Relationships: an output object type can have a relationship to a Postgres table, mapping a field of the output to a table column. The docs state that Action to Postgres database relationships are supported but Action to Remote Schema is not. Example from the docs: an `UpdateAuthorOutput` type with `author_id` gets an object relationship `updatedAuthor` to the `author` table (`field_mapping`: `author_id: id`), so the mutation can return `updatedAuthor { id name }`. Create it in Console `Actions -> [action-name] -> Relationships`, in `custom_types` of actions.yaml, or with `set_custom_types`.

Custom types:
- Object, input object, enum and scalar types may be declared.
- Interfaces and unions are not supported.
- Nested objects (and recursive ones) are supported from v2.2.0.
- Relationships can only use non-list scalar fields, and for nested objects only top-level fields.

Gotcha: the relationship field exists only for roles with a select permission on the related table; for other roles querying it fails with a field-not-found validation error even if the role may run the action.

## Checked

2026-11-04. Confirmed against the cited pages: action-permissions, action-relationships and custom types pages: permissions YAML and API, relationship patterns and Postgres-only database joins, v2.2.0 nested objects, interfaces/unions unsupported, select permission on the related table. Removed or corrected: role-admin sentence, invented `{ id: 1 }` example and the Verify step.

Method: documentation only; no commands were run.
