---
id: computing-software.search-and-information-retrieval.qdrant.search-by-id-and-pagination
name: search-by-id-and-pagination
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [pagination, offset, stable-results, exact, search-paging]
level: practitioner
status: docs-checked
description: "Page through Qdrant results with offset, why approximate search shifts pages, and the exact, client-side and must_not has_id alternatives."
sources:
  - https://qdrant.tech/documentation/search/search/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Search and recommendation APIs skip the first results with `offset`:

```json
{ "query": [0.2, 0.1], "limit": 10, "offset": 20 }
```

Notes from the docs:

- Vector retrieval and HNSW are not designed to be paginated. With `offset`, Qdrant internally retrieves `offset + limit` points but only reads the payload and vectors of the points actually returned, so it saves network and storage access, but deep pages still cost more.
- Search is approximate, so ranking can shift slightly between requests. Paginating with `offset` can then return the same point on several pages or skip points.
- Options the docs give:
  - Retrieve a large batch in one request and paginate on the client (for example fetch the top 100 and show 10 at a time). This avoids repeat round trips and duplicates.
  - Use `params.exact: true` to bypass HNSW and scan all vectors, which gives a stable, deterministic order so offset pagination works (at the cost of a full scan).
  - On later pages add a `must_not` `has_id` filter listing the ids already seen.
- `offset` is not allowed for grouped queries: pagination is not enabled with groups.

To list points matching a filter irrespective of similarity, use scroll, not search offsets.

A query whose `query` is a point id searches for the neighbours of that stored vector, skipping embedding inference.

## Checked

2026-11-08. Confirmed against the Similarity Search page: offset and its cost note, ranking shift under approximate search, the three remedies (client-side batch, exact search, `must_not` `has_id`), groups disallow `offset`, and search by id. Page read by section. Removed unconfirmed claims: the slice filter condition for reproducible sampling, and "the queried point is excluded from results".
Method: documentation only; no commands were run.
