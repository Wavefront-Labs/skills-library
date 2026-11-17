---
id: computing-software.web-development.directus.query-sort-limit-pagination
name: query-sort-limit-pagination
category: computing-software
field: web-development
product: directus
tags: [query-sort, query-limit, pagination, query-limit-max]
level: intro
status: docs-checked
description: "Sort, limit, offset and page Directus API results, including descending sort, relational sort, limit -1 and the QUERY_LIMIT_MAX cap."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/3.query-parameters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```http
GET /items/posts?sort=sort,-date_created,author.name
GET /items/posts?limit=50
GET /items/posts?offset=100
GET /items/posts?page=2
```

- **sort**: comma list in priority order; ascending by default, prefix `-` for descending; dot notation sorts by related field values.
- **limit**: default `100`; `-1` returns all items. Large fetches can degrade performance or time out.
- **QUERY_LIMIT_MAX**: environment variable capping what the API will return; the `limit` parameter cannot override it.
- **offset**: skips N items.
- **page**: alternative to offset, first page is `1`.

SDK: `readItems("posts", { sort: ["-date_created"], limit: 50, page: 2 })`. GraphQL: `posts(limit: 50, page: 2)`.

## Checked

2026-11-04: confirmed against the Directus docs Query Parameters page (Sort, Limit, Offset, Page sections): default limit 100, -1 for all, QUERY_LIMIT_MAX not overridable by limit, page starts at 1. Removed the inferred gotcha and verify line.

Method: documentation only; no commands were run.
