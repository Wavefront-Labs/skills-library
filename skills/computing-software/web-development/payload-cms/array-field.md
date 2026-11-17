---
id: computing-software.web-development.payload-cms.array-field
name: array-field
category: computing-software
field: web-development
product: payload-cms
tags: [array-field, repeating-rows, rowlabel, minrows]
level: practitioner
status: docs-checked
description: "Define array fields for repeating groups of subfields with minRows/maxRows, labels, initCollapsed and a custom RowLabel."
sources:
  - https://payloadcms.com/docs/fields/array
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Array field

Goal: store a repeatable set of subfields.

```ts
{
  name: 'slides',
  type: 'array',
  minRows: 1,
  maxRows: 10,
  labels: { singular: 'Slide', plural: 'Slides' },
  fields: [
    { name: 'title', type: 'text' },
    { name: 'image', type: 'upload', relationTo: 'media' },
  ],
}
```

Options: `name`, `fields` (required), `minRows`, `maxRows`, `labels`, `validate`, `defaultValue`, `localized`, `interfaceName` (generated type name), `dbName`, plus admin `initCollapsed`, `isSortable`, and `components.RowLabel` for a custom row heading.

Gotcha: `unique: true` on a field nested inside an array makes it unique across the whole collection, not per row.

## Checked

2026-11-04. Read fields/array in the payloadcms/payload docs. Confirmed: option list, RowLabel, minRows/maxRows, labels. Removed: the auto-generated row id statement and the REST verify step (not on the page). Added: the nested unique warning.
Method: documentation only; no commands were run.
