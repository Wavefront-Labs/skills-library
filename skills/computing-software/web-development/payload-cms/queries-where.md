---
id: computing-software.web-development.payload-cms.queries-where
name: queries-where
category: computing-software
field: web-development
product: payload-cms
tags: [queries, where-query, operators, and-or]
level: practitioner
status: docs-checked
description: "Write Payload where queries with operators (equals, in, like, contains, exists, near) and combine them with and/or in Local API, REST and GraphQL."
sources:
  - https://payloadcms.com/docs/queries/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Queries and operators

Goal: filter documents the same way in every API.

```ts
const posts = await payload.find({
  collection: 'posts',
  where: {
    and: [
      { color: { equals: 'mint' } },
      { or: [{ price: { less_than: 20 } }, { featured: { equals: true } }] },
    ],
  },
})
```

Operators: `equals`, `not_equals`, `greater_than`, `greater_than_equal`, `less_than`, `less_than_equal`, `like` (case-insensitive, all words), `contains`, `in`, `not_in`, `all` (MongoDB only), `exists`, and for point fields `near`, `within`, `intersects`.

REST uses query strings: `/api/posts?where[color][equals]=mint`. Build complex ones with `qs-esm`:

```ts
import { stringify } from 'qs-esm'
const qs = stringify({ where: { color: { equals: 'mint' } } }, { addQueryPrefix: true })
```

GraphQL: `Posts(where: { color: { equals: mint } }) { docs { color } totalDocs }`.

Gotcha: `near` takes `longitude,latitude,maxDistance,minDistance` (meters, last two optional).

Verify: the same `where` returns the same docs in Local API and REST.

## Checked

2026-11-04. Read queries/overview. Confirmed: the operator list and meanings (equals, not_equals, greater_than, greater_than_equal, less_than, less_than_equal, like as case-insensitive with all words, contains, in, not_in, all for MongoDB only, exists, near with longitude, latitude, maxDistance and minDistance in meters, within, intersects), REST query strings, qs-esm with addQueryPrefix, and the GraphQL where argument. Removed: the statement about access control results being merged into where (not on the page).
Method: documentation only; no commands were run.
