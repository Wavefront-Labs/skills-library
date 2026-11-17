---
id: computing-software.web-development.directus.filter-operators-syntax
name: filter-operators-syntax
category: computing-software
field: web-development
product: directus
tags: [filter-rules, filter-operators, logical-operators, filter-functions]
level: practitioner
status: docs-checked
description: "Write Directus filter rules: field-operator-value syntax, key operators with their restrictions, _and/_or grouping and date functions like year(field)."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/2.filter-rules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filters are used in permissions, validations, automations, APIs and extensions. Syntax: `{ "field": { "operator": "value" } }`.

```json
{ "title": { "_contains": "Directus" } }
```

Operators include `_eq`, `_neq`, `_lt`, `_lte`, `_gt`, `_gte`, `_in`, `_nin`, `_null`, `_nnull`, `_contains` (plus `_icontains` case-insensitive), `_starts_with`, `_ends_with`, `_between`, `_empty`, `_nempty`, and negated `n` variants.

Restrictions:
- `_regex` works only in validation permissions.
- `_some` / `_none` only on One to Many fields.
- `_intersects`, `_intersects_bbox` only on geometry fields.
- `_json` only on JSON fields.
- `_eq`/`_neq` compare numbers and numeric strings loosely.

Group rules with `_and` / `_or` arrays; they nest directly in each other but not inside other field rules:

```json
{ "_or": [ { "status": { "_eq": "published" } }, { "user_created": { "_eq": "$CURRENT_USER" } } ] }
```

Functions in keys: `"year(published_date)": { "_eq": 1968 }`, `"month(published_date)": { "_eq": 4 }`.

## Checked

2026-11-04: confirmed against the Directus docs Filter Rules page: operator table and footnote restrictions, filter syntax, logical operator nesting rule, function parameters example. Removed the unsupported verify line.

Method: documentation only; no commands were run.
