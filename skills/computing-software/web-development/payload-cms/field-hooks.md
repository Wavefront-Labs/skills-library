---
id: computing-software.web-development.payload-cms.field-hooks
name: field-hooks
category: computing-software
field: web-development
product: payload-cms
tags: [field-hooks, field-beforechange, beforeduplicate, computed-field]
level: practitioner
status: docs-checked
description: "Use field-level beforeValidate, beforeChange, beforeDuplicate, afterChange and afterRead hooks to transform single field values."
sources:
  - https://payloadcms.com/docs/hooks/fields
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Field hooks

Goal: transform one field's value during an operation.

```ts
{
  name: 'name',
  type: 'text',
  hooks: {
    beforeValidate: [({ value }) => value],
    beforeChange: [({ value }) => value],
    beforeDuplicate: [({ value }) => `${value} copy`],
    afterChange: [({ value }) => {}],
    afterRead: [({ value }) => value],
  },
}
```

Field hooks may modify the return value of the field before the operation continues. They receive `value`, `data`, `siblingData`, `field`, `collection` (or `global`), `context`, `operation`, `originalDoc`, `previousValue`, `req` and `findMany` (in `afterRead`, whether a find-many or find-one is running).

`beforeValidate` and `beforeChange` also run with `operation: 'validate'` during on-demand validation; `afterChange` does not. The page says `beforeChange` runs immediately before validation, so treat `value` as unvalidated.

Gotcha: because GraphQL is typed, changing the TYPE of data returned from a field hook produces errors in the GraphQL API. To change the shape of data use collection or global hooks instead.

`beforeDuplicate` runs when a document is duplicated and lets you alter the copied value (for example to keep a unique field unique). It runs before `beforeValidate` and `beforeChange`. For unique required text fields Payload appends '- Copy' by default unless your field defines its own hook, and the hook does not run for a field with `disableDuplicate`.

## Checked

2026-11-04. Read hooks/fields in the payloadcms/payload docs. Confirmed: hook list, arguments, GraphQL typing warning, beforeDuplicate behaviour. Added: validate operation notes, beforeDuplicate ordering and default. Flagged: same beforeChange wording as hooks/collections. Removed: the verify step.
Method: documentation only; no commands were run.
