---
id: computing-software.web-development.ghost.ghost-content-api-query-parameters
name: ghost-content-api-query-parameters
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, limit, page, order, fields, formats, query-parameters]
level: practitioner
status: docs-checked
description: "Ghost Content API query parameters: include, fields, formats, filter, limit, page and order, with defaults and per-resource sort orders."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/parameters.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shape Content API responses with query parameters.

All endpoints accept `include` and `fields`. Browse endpoints also accept `filter`, `limit`, `page` and `order`. Values must be URL encoded when you build the URL yourself; the client libraries handle encoding for you.

- `include`: related data, comma separated and combinable (`&include=authors,tags`). Available: `authors`, `tags` for posts and pages; `count.posts` for authors and tags; `monthly_price`, `yearly_price`, `benefits` for tiers. For posts and pages, `authors` adds `authors` and `primary_author`, `tags` adds `tags` and `primary_tag`; `count.posts` adds `"count": {"posts": 7}`-style data.
- `fields`: limit the keys returned, for example `&fields=title,url` (the sample response still carries `id`). Useful for optimising queries but does not play well with `include`.
- `formats`: posts and pages only. By default only `html` is returned; each post and page has two formats, `html` and `plaintext`, and `&formats=html,plaintext` additionally returns `plaintext`.
- `filter`: browse requests only, for example `&filter=featured:true` or `&filter=tag:getting-started` on posts, `&filter=visibility:public` on tiers. The page says query strings are explained in the filtering section.
- `limit`: browse only. 15 records by default; `&limit=5` returns 5; `&limit=100` returns 100, the maximum.
- `page`: browse only. The first 15 records by default; `&page=2` returns the second set of 15.
- `order`: browse only; defaults differ by resource. Posts `published_at DESC` (newest first), pages `title ASC`, tags `name ASC`, authors `name ASC`, tiers `monthly_price ASC`. Syntax follows SQL order by: `&order=published_at%20asc` returns the newest post last.

Example query string: `&limit=5&order=published_at%20asc&include=tags`.

Gotcha: 100 is the maximum `limit`, so larger exports must page through results with `page`.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text of the docs repo file, about 100 lines, no imported snippets present): content-api/parameters.mdx. Every parameter, default, maximum, include value and sort order above matches it. Removed: the claim that the `{{#get}}` helper encodes values (page mentions client libraries only), the full request path in the example (the page gives only query strings), and the Verify step on `meta.pagination.limit` (that page was not among the sources). Added the authors and tiers default sort orders and the include result fields from the page.
Method: documentation only; no commands were run.
