---
id: computing-software.web-development.strapi.attribute-types-validations
name: attribute-types-validations
category: computing-software
field: web-development
product: strapi
tags: [strapi, attributes, validations, required, private, minlength, schema]
level: practitioner
status: docs-checked
description: "Strapi attribute types and basic validation parameters (required, min, max, minLength, maxLength, private, configurable)."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Attribute types and validations

Every attribute has a `type`:

- String: `string`, `text`, `richtext`, `enumeration`, `email`, `password`, `uid`
- Date: `date`, `time`, `datetime`, `timestamp`
- Number: `integer`, `biginteger`, `float`, `decimal`
- Other: `boolean`, `json`
- Strapi-specific: `media`, `relation`, `customField`, `component`, `dynamiczone`
- i18n-only: `locale`, `localizations`

## Validation parameters
| Param | Meaning | Default |
|---|---|---|
| `required` | adds a required validator | `false` |
| `max` | value must be >= the given maximum (as worded on the page) | - |
| `min` | value must be <= the given minimum (as worded on the page) | - |
| `minLength` / `maxLength` | characters in an input value | - |
| `private` | removed from the server response | `false` |
| `configurable` | `false` hides it from the Content-type Builder | `true` |

```json
"attributes": {
  "title": { "type": "string", "minLength": 3, "maxLength": 99, "unique": true },
  "description": { "default": "My description", "type": "text", "required": true },
  "slug": { "type": "uid", "targetField": "title" }
}
```

Use `private: true` for sensitive data.

`uid` accepts `targetField` (auto-generates the value from that field) and `options` (passed to the underlying slugify generator; the result must match `/^[A-Za-z0-9-_.~]*$`). The i18n types `locale` and `localizations` are only usable when i18n is enabled on the content-type.

Draft & Publish and `unique`: with Draft & Publish on, Strapi skips `unique` checks on draft saves, so duplicates only fail at publish time. The docs suggest disabling Draft & Publish where global uniqueness is required, adding custom validation (lifecycle hooks or middleware), or relying on a generated `uid`.

An experimental, advanced-only `column` object per attribute passes options to Knex during migrations: `name`, `defaultTo`, `notNullable`, `unsigned`, `unique`, `type` and `args` (for example `"type": "decimal", "args": [6,1]`). The docs warn it may break features and will not be made stable.

## Checked
Confirmed 2026-11-08 against the Strapi models page: the attributes, validations and uid sections (the model attributes through uid area, read in full); the relations, components, lifecycle and later sections were not needed for this skill. Added uid, unique with Draft & Publish and the experimental column settings. The page's wording for `max` and `min` is kept as the page words it.
Method: docs-only read of cited pages, 2026-11-08
