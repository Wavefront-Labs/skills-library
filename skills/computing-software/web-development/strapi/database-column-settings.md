---
id: computing-software.web-development.strapi.database-column-settings
name: database-column-settings
category: computing-software
field: web-development
product: strapi
tags: [strapi, column, knex, notnullable, unique, draft-and-publish, schema]
level: advanced
status: docs-checked
description: "Per-attribute column settings passed to Knex, and why unique is not checked on drafts when Draft and Publish is on."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database validations and settings (`column`)

Advanced use only; they may break features and the docs say there are no plans to make them stable. They are passed to the Knex.js `tableBuilder` during schema migrations.

| Param | Meaning | Default |
|---|---|---|
| `name` | column name in the database | - |
| `defaultTo` | database default, typically with `notNullable` | - |
| `notNullable` | column cannot be null | `false` |
| `unsigned` | numbers only; no negatives, doubles max length | `false` |
| `unique` | database-level uniqueness on published entries | `false` |
| `type` | database type; arguments go in `args` | - |
| `args` | arguments passed to the Knex function | `[]` |

```json
"title": {
  "type": "string",
  "minLength": 3,
  "maxLength": 99,
  "unique": true,
  "column": {
    "unique": true // enforce database unique also
  }
}
```

## Draft and Publish trap
With Draft & Publish on, `unique` is skipped while saving a draft, so duplicates fail only at publish time. To avoid it: disable Draft & Publish on globally unique types, add custom validation (lifecycle hook or middleware) that checks drafts, or rely on a `uid` field and editorial conventions.

## Checked

2026-11-04: checked against the Strapi docs page Models (backend-customization/models), section Database validations and settings. Confirmed: experimental and advanced-use warning, Knex.js `tableBuilder` during schema migrations, all seven parameters with defaults, the unique-on-published behaviour, the Draft & Publish caution and its three workarounds, the example. Removed: nothing.

Method: documentation only; no commands were run.
