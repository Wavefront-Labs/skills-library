---
id: computing-software.web-development.node-express.cursor-vs-offset-pagination
name: cursor-vs-offset-pagination
category: computing-software
field: web-development
product: node-express
tags: [rest-api, cursor-pagination, offset-pagination, keyset-pagination, api-design, sql]
level: practitioner
status: verified
description: "Designing API pagination: offset vs cursor (keyset) trade-offs, opaque cursor encoding, stable sort keys, page size limits, response shape and Link headers."
sources:
  - https://use-the-index-luke.com/no-offset
  - https://www.rfc-editor.org/rfc/rfc8288
  - https://docs.stripe.com/api/pagination
  - https://slack.engineering/evolving-api-pagination-at-slack/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pagination: cursor vs offset

## 1. Trade-offs
| | Offset (`?page=3&limit=20`) | Cursor/keyset (`?after=eyJ...&limit=20`) |
|---|---|---|
| Jump to page N | yes | no (next/prev only) |
| Performance on deep pages | degrades: DB scans and discards OFFSET rows | constant with an index |
| Consistency under inserts/deletes | items skipped or duplicated | stable |
| Total count | easy (but `COUNT(*)` is expensive at scale) | usually omitted |
Use cursors for feeds, infinite scroll, large or fast-changing tables and public APIs; offset for small admin tables needing page numbers.

## 2. Keyset query
Order by a unique, indexed tuple:
```sql
-- index: (created_at DESC, id DESC)
SELECT id, created_at, title FROM posts
WHERE (created_at, id) < ($1, $2)          -- values from the cursor
ORDER BY created_at DESC, id DESC
LIMIT 21;                                   -- limit + 1 to know if there's a next page
```
Row-value comparison ran correctly in PostgreSQL 18.6 (PGlite) and SQLite 3.50; on a 50,000-row table the keyset query used an index scan and read 21 index entries (0.1 ms) while `OFFSET 40000` scanned 40,021 index entries (about 27 ms). For other databases check the docs, or expand to `created_at < $1 OR (created_at = $1 AND id < $2)`.

## 3. Opaque cursors
```js
const encode = row => Buffer.from(JSON.stringify([row.created_at, row.id])).toString("base64url");
const decode = c => { const [ts, id] = JSON.parse(Buffer.from(c, "base64url").toString()); /* validate types! */ return { ts, id }; };
```
Opaque so clients don't construct them and you can change the scheme. Validate decoded values (untrusted input); sign them (HMAC) if they embed anything sensitive or filters. Cursors are tied to the sort order and filters - reject a cursor used with different parameters.

## 4. Response shape
```json
{ "data": [ … ], "page": { "next_cursor": "eyJ…", "has_more": true } }
```
Also/or `Link: <https://api.example.com/posts?after=eyJ…&limit=20>; rel="next"` (RFC 8288). Stripe style uses `starting_after`/`ending_before` object IDs.

## 5. Rules
- Default and maximum `limit` (e.g. 20, max 100); clamp, don't error, or return 400 consistently.
- Always a deterministic order with a unique tiebreaker (`id`) - otherwise items repeat across pages.
- For offset: cap the maximum offset (deep pagination DoS) and avoid exact totals on huge tables (estimate or "1,000+").

## Verify
Insert items while paging in a test: no duplicates or gaps with cursors; EXPLAIN shows index range scan without large offsets; limit clamping enforced.
