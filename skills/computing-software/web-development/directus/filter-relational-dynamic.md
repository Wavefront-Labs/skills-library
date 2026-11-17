---
id: computing-software.web-development.directus.filter-relational-dynamic
name: filter-relational-dynamic
category: computing-software
field: web-development
product: directus
tags: [relational-filter, dynamic-variables, some-none, follow-syntax]
level: advanced
status: docs-checked
description: "Filter Directus items through M2O, M2M and O2M relations, use _some and _none, dynamic variables like $CURRENT_USER and $NOW, and $FOLLOW."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/2.filter-rules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**M2O**: nest the related field: `{ "author": { "name": { "_eq": "Rijk" } } }`.

**M2M**: the filter goes through the junction collection: `{ "authors": { "authors_id": { "name": { "_eq": "Rijk" } } } }`.

**O2M / M2M with _some and _none**: `_some` (the default) matches when at least one related item meets the condition; `_none` when no related item does.

```json
{ "categories": { "_none": { "name": { "_eq": "Recipe" } } } }
```

**Dynamic variables**: `$CURRENT_USER`, `$CURRENT_ROLE`, `$NOW`, and `$NOW(<adjustment>)` such as `$NOW(-1 year)` or `$NOW(+2 hours)`. In permissions you can reach related fields, e.g. `$CURRENT_ROLE.name`, `$CURRENT_USER.avatar.filesize`.

```json
{ "owner": { "_eq": "$CURRENT_USER" } }
```

**$FOLLOW(target-collection, relation-field)** queries an indirect relation when the current collection has no field pointing to the target:

```json
{ "name": "Germany", "$FOLLOW(cities, country_id)": { "name": "Berlin" } }
```

## Checked

2026-11-04: confirmed against the Directus docs Filter Rules page: Many-to-One and Many-to-Many nesting, _some default and _none, dynamic variables and nested permission variables, $FOLLOW syntax. Removed the unsupported verify line.

Method: documentation only; no commands were run.
