---
id: computing-software.search-and-information-retrieval.apache-solr.cursormark-deep-paging
name: cursormark-deep-paging
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [deep-paging, cursormark, nextcursormark, uniquekey-sort, pagination]
level: advanced
status: docs-checked
description: "Page deeply through Solr results with cursorMark: start with *, pass nextCursorMark back, sort must include the uniqueKey, and handle partialResults and replica score differences."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/pagination-of-results.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cursormark-deep-paging

Send `cursorMark=*` on the first request together with a `sort`. The response contains `nextCursorMark`; pass it as `cursorMark` on the next request and repeat. Stop when you have enough, or when the returned `nextCursorMark` equals the `cursorMark` you sent and `partialResults` is no longer true in the response header. If `partialResults` is true, matching marks do not prove there are no more results.

Constraints:
- `cursorMark` and `start` are mutually exclusive.
- `sort` must include the `uniqueKey` field (asc or desc). If `id` is the key, `id asc` or `name asc, id desc` works; `name asc` alone does not.
- Sorting on `score` is risky in multi-replica SolrCloud: different replicas can have different scores, so a series of requests served by different replicas may skip or repeat documents. Use PULL replicas, or keep all requests of one series on the same replica.
- Ties on sort values are broken by the uniqueKey, so documents sharing values are not skipped.

Cursors are stateless on the server; no resources are held between requests.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Pagination of Results page: `cursorMark=*`, `nextCursorMark`, mutual exclusion with `start`, the uniqueKey sort rule and its `id asc` / `name asc, id desc` examples, the partialResults caveat, PULL replicas or one replica for score sorts, and stateless cursors. Nothing removed.

Method: documentation only; no commands were run.
