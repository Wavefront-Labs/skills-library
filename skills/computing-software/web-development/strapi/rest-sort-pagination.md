---
id: computing-software.web-development.strapi.rest-sort-pagination
name: rest-sort-pagination
category: computing-software
field: web-development
product: strapi
tags: [strapi, rest-api, sort, pagination, pagesize, limit, withcount]
level: practitioner
status: docs-checked
description: "Sort Strapi REST results on several fields and paginate by page/pageSize or by start/limit, with defaults and limits."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest/sort-pagination.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sort and pagination

## Sort
- One field: `GET /api/:pluralApiId?sort=value`
- Several: `GET /api/:pluralApiId?sort[0]=value1&sort[1]=value2`
- `:asc` (default, may be omitted) or `:desc`.

```bash
curl 'http://localhost:1337/api/restaurants?sort[0]=Description:asc&sort[1]=Name:desc' \
  -H 'Authorization: Bearer <token>'
```

With `qs`: `sort: ['Description:asc', 'Name:desc']`.

## Pagination: pick one method, never mix
By page:

| Param | Default |
|---|---|
| `pagination[page]` | 1 |
| `pagination[pageSize]` | 25 |
| `pagination[withCount]` | true (adds totals) |

```
/api/articles?pagination[page]=1&pagination[pageSize]=10
```

By offset: `pagination[start]` (default 0), `pagination[limit]` (default 25), `pagination[withCount]`.

```
/api/articles?pagination[start]=0&pagination[limit]=10
```

Response `meta.pagination` carries `page`, `pageSize`, `pageCount`, `total` for page pagination, and `start`, `limit`, `total` for offset pagination.

Default and maximum `limit` are set in `./config/api.js` via `api.rest.defaultLimit` and `api.rest.maxLimit`.

## Checked

2026-11-04: checked against the Strapi docs page REST API: Sort & Pagination (api/rest/sort-pagination) and API calls configuration (configurations/api). Confirmed: sort syntaxes and `:asc`/`:desc`, no mixing of pagination methods, all parameters and defaults (1, 25, true, 0, 25), `api.rest.defaultLimit` and `api.rest.maxLimit`. Corrected: the meta.pagination keys differ between page and offset methods.

Method: documentation only; no commands were run.
