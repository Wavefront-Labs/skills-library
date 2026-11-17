---
id: computing-software.web-development.directus.query-deep-alias
name: query-deep-alias
category: computing-software
field: web-development
product: directus
tags: [query-deep, query-alias, nested-query, alias-limits]
level: advanced
status: docs-checked
description: "Apply query parameters to nested relational data with deep and fetch one relation several times under different names with alias."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/3.query-parameters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**deep** sets any other query parameter (except `fields` and `deep` itself) on a nested relation. Prefix the nested parameters with an underscore.

```http
GET /items/posts?deep[translations][_filter][languages_code][_eq]=en-US
```

Nested limits and sorts:

```json
{ "deep": { "related_posts": { "_limit": 3, "comments": { "_sort": "rating", "_limit": 1 } } } }
```

**alias** renames fields for this request and fetches the same relation multiple times with different filters:

```http
GET /items/posts?alias[all_translations]=translations&alias[dutch_translations]=translations
  &deep[dutch_translations][_filter][code][_eq]=nl-NL
```

Aliases can wrap functions, e.g. `alias[release_year]=year(released)`, and appear in deep as `deep[author][_alias][birthyear]=year(birthday)`.

Limits: no aliases on relational paths (`alias[x]=author.name` fails), and no `.` inside an alias name. GraphQL supports both natively through field aliases and arguments.

## Checked

2026-11-04: confirmed against the Directus docs Query Parameters page (Deep and Alias sections): underscore-prefixed nested parameters, related_posts limit and sort example, alias examples, alias limits. Removed the unsupported verify line.

Method: documentation only; no commands were run.
