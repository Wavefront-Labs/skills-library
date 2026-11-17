---
id: computing-software.software-engineering.api-design.offset-pagination-and-total-counts
name: offset-pagination-and-total-counts
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, offset-pagination, total-count, pagination, keyset-pagination, aip-158]
level: practitioner
status: docs-checked
description: "Know the cost and drift problems of offset pagination, why AIP-158 uses opaque page tokens, and how to treat total counts (optional, may be an estimate)."
sources: ["https://google.aip.dev/158", "https://use-the-index-luke.com/no-offset", "https://www.postgresql.org/docs/current/queries-limit.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offset pagination and total counts

## Offset problems
- **Cost**: the database must still fetch and order the skipped rows before returning later ones; PostgreSQL's
  manual says rows skipped by OFFSET still have to be computed, so a large OFFSET might be inefficient.
- **Drift**: a row inserted between fetching two pages gives duplicates on the next offset page (and other
  anomalies are possible).
- Rows are only well defined with an `ORDER BY`; use a deterministic order for stable pages.
- Keyset (seek) pagination, a `WHERE` clause selecting only unseen data, avoids drift and is faster. Offset
  mostly survives because tools support it and keyset needs more work.

## AIP-158 style pagination
- Request: `int32 page_size` (maximum number of results, service may return fewer) and string `page_token`
  (not required).
- Response: `next_page_token`; an empty token is the only way to signal end of collection.
- If `page_size` exceeds the API maximum, coerce down; a negative value is an `INVALID_ARGUMENT` error.
- Page tokens must be opaque, URL-safe and not user-parseable, so pagination internals can change without
  breaking users. Base-64 encoding a transparent token is not sufficient obfuscation. Tokens held in a database
  may expire after a reasonable time.
- Adding pagination later changes behaviour for old clients if the new default page size is smaller than what
  was previously returned (AIP-180).

## Total counts
- AIP-158: `total_size` (int32) is optional ("may"), and may be an estimate, which the API should document.
- A count over a large filtered set can cost as much as the query: make it optional, or omit it and rely on
  `next_page_token` to signal more data.

## Checked
Date: 2026-11-01. Confirmed on AIP-158 (page_size, page_token, next_page_token, coercion, negative size, opaque
tokens, total_size optional and estimate), Use The Index, Luke (offset cost, duplicates, keyset) and the
PostgreSQL LIMIT/OFFSET manual page. Removed: concrete offset caps, SQL snippets, count-endpoint, estimate
and capped-count recipes, which the cited pages do not state.
Method: documentation only; no commands were run.
