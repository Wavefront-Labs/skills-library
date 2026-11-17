---
id: computing-software.web-development.payload-cms.fields-overview
name: fields-overview
category: computing-software
field: web-development
product: payload-cms
tags: [fields, field-types, validate, condition]
level: practitioner
status: docs-checked
description: "Use field config basics: common options, validate functions, conditional logic with admin.condition, default values and field names."
sources:
  - https://payloadcms.com/docs/fields/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fields overview

Goal: use the options shared by all field types.

Options documented on the overview page: `type` (required), `name` (data fields), `defaultValue`, `validate`, `hooks`, `access`, `admin`, `virtual`, `disableDuplicate`. Options such as `required`, `unique`, `index` and `localized` are documented on the individual field pages.

Custom validation (runs in the Admin Panel and on the server):

```ts
{
  name: 'title',
  type: 'text',
  validate: (value, { data, siblingData, operation, path, id, req, event }) =>
    value?.length > 3 || 'Title is too short',
}
```

Return `true` or an error string. `event` is `onChange` or `submit` and is a performance opt-in.

Conditional logic:

```ts
admin: {
  condition: (data, siblingData, { blockData, path, user }) =>
    Boolean(data.enableGreeting),
}
```

Admin options include `description`, `position`, `width`, `style`, `className`, `readOnly`, `disabled`, `hidden`, `components`, `condition`.

A field `name` is the property name in the database and API. It must be unique among siblings and should follow JavaScript identifier rules (no leading digit, no hyphens). `__v`, `salt`, `hash` and `file` are reserved, and `status` is reserved with Postgres when drafts are enabled. Field components (`Field`, `Cell`, `Filter`, `Label`, `Error`, `Diff`, `Description`, `beforeInput`, `afterInput`) can be swapped for custom ones.

`virtual: true` fields are not stored (compute them with hooks); `virtual: 'author.name'` resolves through a relationship at query time.

## Checked

2026-11-04. Read fields/overview in the payloadcms/payload docs. Confirmed: validate arguments and return, condition arguments, admin options, custom components list, name rules. Removed: the common-options list entries saveToJWT, custom and jsonSchema (not on this page; localized, index, unique, required and label are documented on field pages instead) and the verify step. Added: reserved names, virtual fields.
Method: documentation only; no commands were run.
