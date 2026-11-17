---
id: computing-software.web-development.payload-cms.collection-hooks
name: collection-hooks
category: computing-software
field: web-development
product: payload-cms
tags: [collection-hooks, beforechange, afterchange, beforevalidate]
level: practitioner
status: docs-checked
description: "Use collection hooks beforeOperation, beforeValidate, beforeChange, afterChange, beforeRead, afterRead, delete hooks and auth hooks."
sources:
  - https://payloadcms.com/docs/hooks/collections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collection hooks

Goal: run logic at document lifecycle events.

```ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  hooks: {
    beforeOperation: [({ args, operation }) => args],
    beforeValidate: [({ data }) => data],
    beforeChange: [({ data, operation }) => data],
    afterChange: [({ doc, previousDoc, operation }) => doc],
    beforeRead: [({ doc }) => doc],
    afterRead: [({ doc }) => doc],
    beforeDelete: [],
    afterDelete: [],
    afterOperation: [],
    afterError: [],
  },
  fields: [],
}
```

Order of use:

- `beforeValidate` runs on `create`, `update` and `validate`; format incoming data before server-side validation.
- `beforeChange`: the page describes it as running immediately before validation, so treat `data` as unvalidated input (required fields can be missing). Return the (modified) `data`. It also runs with `operation: 'validate'`; `afterChange` does not.
- `afterChange` receives `doc` (result), `previousDoc` and `data`.
- `beforeRead` fires before hidden fields are removed and before locales are flattened; `afterRead` is the last step before documents return.

Return values of `beforeDelete` and `afterDelete` are discarded.

Common arguments: `collection`, `context`, `req`, `operation`, and `originalDoc` (undefined on create).

Auth-enabled collections add `beforeLogin`, `afterLogin`, `afterLogout`, `afterMe`, `afterRefresh`, `afterForgotPassword`, `refresh` and `me`.

## Checked

2026-11-04. Read hooks/collections and hooks/overview in the payloadcms/payload docs. Confirmed: hook list, arguments, auth hooks, beforeRead/afterRead ordering. Fixed: the skill said beforeChange runs after validation, but the page says it runs immediately before validation. Flagged: that wording conflicts with the usual after-validation reading, so the skill states what the page says. Removed: the verify step.
Method: documentation only; no commands were run.
