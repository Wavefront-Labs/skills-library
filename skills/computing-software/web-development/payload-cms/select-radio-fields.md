---
id: computing-software.web-development.payload-cms.select-radio-fields
name: select-radio-fields
category: computing-software
field: web-development
product: payload-cms
tags: [select-field, radio-field, options, enumname]
level: intro
status: docs-checked
description: "Define select fields with options, hasMany, filterOptions and enumName, and know radio options."
sources:
  - https://payloadcms.com/docs/fields/select
  - https://payloadcms.com/docs/fields/radio
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Select and radio fields

Goal: constrain a value to a fixed list.

```ts
{
  name: 'status',
  type: 'select',
  options: [
    { label: 'Draft', value: 'draft' },
    { label: 'Published', value: 'published' },
  ],
  defaultValue: 'draft',
  required: true,
}
```

Select options: `options` (required), `hasMany`, `filterOptions`, `enumName` and `dbName` (SQL enum naming), `interfaceName`, `index`, `unique`, `localized`, `saveToJWT`, plus admin `isClearable`, `isSortable`, `placeholder`.

Options may be plain strings or `{ label, value }` objects.

`radio` takes `options` the same way and renders radio buttons with a single value.

`enumName` names the enum and `dbName` the table (used when `hasMany` is true) with an SQL adapter; both are generated from the field name if omitted. Option values should be strings without hyphens or special characters (underscores are fine) because of GraphQL enum naming.

Verify: the Admin Panel dropdown lists only the declared options.

## Checked

2026-11-04. Read fields/select and fields/radio. Confirmed: options as strings or label and value objects, hasMany, filterOptions, enumName, dbName, interfaceName, index, unique, localized, saveToJWT, defaultValue, required, admin isClearable, isSortable and placeholder, and radio as single-value selection from options. Added: the GraphQL enum value restriction from the select page.
Method: documentation only; no commands were run.
