---
id: computing-software.web-development.payload-cms.query-pagination
name: query-pagination
category: computing-software
field: web-development
product: payload-cms
tags: [pagination, limit, page, totaldocs]
level: intro
status: docs-checked
description: "Paginate find results with limit, page and pagination, and read docs, totalDocs, totalPages and related response metadata."
sources:
  - https://payloadcms.com/docs/queries/pagination
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pagination

Goal: page through results.

Controls: `limit` (default `10` when pagination is enabled), `page` (default `1`), `pagination` (default `true`; `false` skips count queries and page calculation but still honours a positive `limit`).

```ts
const posts = await payload.find({ collection: 'posts', limit: 10, page: 2 })
```

REST: `/api/posts?limit=10&page=2`.

Response shape: `docs` plus `totalDocs`, `limit`, `totalPages`, `page`, `pagingCounter`, `hasPrevPage`, `hasNextPage`, `prevPage`, `nextPage`.

Tips:

- Use `pagination: false` for big exports or when you do not need counts; it avoids the extra count query.
- Collections can set `admin.pagination` defaults for the List View.

Verify: `totalPages` equals `ceil(totalDocs / limit)`.

## Checked

2026-11-04. Read queries/pagination and configuration/collections. Confirmed: limit default 10, page default 1, pagination default true and false disabling count queries while honouring a limit, the Local API and REST usage, the response properties (docs, totalDocs, limit, totalPages, page, pagingCounter, hasPrevPage, hasNextPage, prevPage, nextPage), and admin.pagination for the List View.
Method: documentation only; no commands were run.
