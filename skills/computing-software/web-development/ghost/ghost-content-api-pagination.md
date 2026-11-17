---
id: computing-software.web-development.ghost.ghost-content-api-pagination
name: ghost-content-api-pagination
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, pagination, meta, limit, page]
level: intro
status: docs-checked
description: "Page through Ghost Content API browse results using the page and limit parameters and the meta.pagination object."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/pagination.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: walk a full collection of records from the Ghost Content API.

All browse endpoints are paginated and return 15 records by default. Use `limit` (maximum 100) and `page` to move through results. Every browse response carries `meta.pagination` with these keys: `page`, `limit`, `pages` (total pages), `total`, `next` and `prev`. The documented example shows `next` and `prev` as `null` for a single page of results.

Loop pattern:
1. Request `?limit=100&page=1`.
2. Read `meta.pagination.pages`.
3. Request each following page number up to that count.

Example response metadata for a single page of results: `{"page":1,"limit":2,"pages":1,"total":1,"next":null,"prev":null}`.

Notes:
- The JavaScript client resolves browse calls to an array that also has a `meta` property, so the same loop works with `posts.browse({limit: 100, page})`.
- The Admin API uses the same pagination shape and parameters.

Verify: summing the records from all pages equals `meta.pagination.total`.

## Checked

2026-11-04. Confirmed: 15 default records, page and limit, limit maximum 100, meta.pagination keys, the example metadata, Admin API sharing the shape (pagination, parameters and Admin API overview pages). Removed: the claim that next and prev are page numbers, and the totals-can-shift advice.

Method: documentation only; no commands were run.
