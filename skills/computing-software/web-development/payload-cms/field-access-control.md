---
id: computing-software.web-development.payload-cms.field-access-control
name: field-access-control
category: computing-software
field: web-development
product: payload-cms
tags: [field-access, field-permissions, hide-field, role-based]
level: practitioner
status: docs-checked
description: "Restrict individual fields with access.create, read, update and validate functions that return booleans."
sources:
  - https://payloadcms.com/docs/access-control/fields
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Field access control

Goal: hide or protect single fields per user.

```ts
{
  name: 'internalNotes',
  type: 'text',
  access: {
    create: ({ req: { user } }) => user?.role === 'admin',
    read: ({ req: { user } }) => user?.role === 'admin',
    update: ({ req: { user } }) => user?.role === 'admin',
  },
}
```

- `create` - may a value be set when creating? If false, passed values are discarded.
- `read` - may the field value be read? If false the field is omitted from the response.
- `update` - may the value be changed?
- `validate` - optionally overrides `update` for candidate data during on-demand validation.

Argument properties include `req` (with `user`), `collection` or `global` (the owning config), `data`, `siblingData`, `id` and `doc` where relevant.

Gotcha: field access functions must return a boolean. Unlike collection access they cannot return query constraints.

A denied `create` or `update` does not throw: the value is discarded and the stored value stays unchanged. A denied `read` omits the property. Inside blocks the arguments also include `blockData` (the nearest parent block row).

## Checked

2026-11-04. Read access-control/fields in the payloadcms/payload docs. Confirmed: create, read, update, validate, argument properties, no query constraints (page banner). Added: silent-discard behaviour and blockData. Removed: the verify step.
Method: documentation only; no commands were run.
