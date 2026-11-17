---
id: computing-software.web-development.payload-cms.text-and-number-fields
name: text-and-number-fields
category: computing-software
field: web-development
product: payload-cms
tags: [text-field, number-field, textarea, hasmany]
level: intro
status: docs-checked
description: "Configure text, textarea and number fields with length limits, min/max, hasMany and minRows/maxRows."
sources:
  - https://payloadcms.com/docs/fields/text
  - https://payloadcms.com/docs/fields/number
  - https://payloadcms.com/docs/fields/textarea
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Text, textarea and number fields

Goal: define scalar inputs.

```ts
{ name: 'title', type: 'text', required: true, minLength: 3, maxLength: 80, unique: true },
{ name: 'keywords', type: 'text', hasMany: true, minRows: 1, maxRows: 5 },
{ name: 'price', type: 'number', min: 0, max: 100000, admin: { step: 0.01 } },
```

Text options: `unique`, `minLength`, `maxLength`, `hasMany`, `minRows`, `maxRows`, `index`, `saveToJWT`, `defaultValue`, `localized`, `required`, plus admin options `placeholder`, `autoComplete`, `rtl`.

Number options: `min`, `max`, `hasMany`, `minRows`, `maxRows`, plus admin `step`, `placeholder`, `autoComplete`.

Related scalar types: `textarea` (same length options), `email`, `checkbox`, `code`, `json`, `radio` and `point`.

- `unique: true` creates a database-level unique index.
- `hasMany` stores an array of values; `minRows`/`maxRows` apply only with `hasMany`.
- `index: true` is recommended for fields users filter or sort by.

Verify: saving a 2-character title fails validation with a length message.

## Checked

2026-11-04. Read fields/text, fields/number and fields/textarea (plus the field pages for email, checkbox, code, json, radio and point exist). Confirmed: text options (unique as a database-level unique index, minLength, maxLength, hasMany, minRows, maxRows, index, saveToJWT, defaultValue, localized, required) and admin options (placeholder, autoComplete, rtl); number options (min, max, hasMany, minRows, maxRows) and admin step, placeholder and autoComplete; textarea length options; minRows and maxRows used with hasMany.
Method: documentation only; no commands were run.
