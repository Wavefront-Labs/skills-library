---
id: computing-software.web-development.payload-cms.rest-api
name: rest-api
category: computing-software
field: web-development
product: payload-cms
tags: [rest-api, crud-endpoints, api-routes, method-override]
level: practitioner
status: docs-checked
description: "Use the REST API at /api: CRUD routes per collection, shared query parameters, auth routes, globals and GET method override."
sources:
  - https://payloadcms.com/docs/rest-api/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REST API

Goal: call Payload over HTTP.

Collections are mounted by slug (kebab-case) under `/api`:

- `GET /api/{collection}` find (paginated), `GET /api/{collection}/{id}` find by ID, `GET /api/{collection}/count`.
- `POST /api/{collection}` create, `PATCH /api/{collection}` bulk update with `where`, `PATCH /api/{collection}/{id}` update, `DELETE` for bulk and single delete.
- Auth routes under `/api/{user-collection}/` (login, logout, me, refresh-token, verify, forgot-password, reset-password, unlock).
- Globals: `GET` and `POST /api/globals/{global-slug}`.
- Preferences: `/api/payload-preferences/{key}`.

Query parameters shared across routes: `depth`, `locale`, `fallback-locale`, `select`, `populate`, `limit`, `page`, `sort`, `where`, `joins`.

Long query strings can exceed URL limits. Send a POST with the override header and a form-encoded body:

```ts
await fetch(`${api}/${collectionSlug}`, {
  method: 'POST',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Payload-HTTP-Method-Override': 'GET',
  },
  body: qs.stringify({ depth: 1, locale: 'en' }),
})
```

Verify: `GET /api/<slug>?limit=1` returns `docs` and paging metadata.

## Checked

2026-11-04. Read rest-api/overview. Confirmed: collections mounted by kebab-case slug under /api, the find, findByID, count, create, bulk and single update, bulk and single delete routes, the auth routes (login, logout, unlock, refresh-token, verify, me, forgot-password, reset-password), global routes, payload-preferences routes, the shared query parameters (depth, locale, fallback-locale, select, populate, limit, page, sort, where, joins), and the X-Payload-HTTP-Method-Override: GET method with a form-encoded body.
Method: documentation only; no commands were run.
