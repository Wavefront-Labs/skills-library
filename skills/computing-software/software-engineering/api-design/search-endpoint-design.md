---
id: computing-software.software-engineering.api-design.search-endpoint-design
name: search-endpoint-design
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, search-api, full-text-search, aip-160, query-parameters, filtering]
level: practitioner
status: docs-checked
description: "Design search endpoints: GET vs POST, query and filter parameters, relevance ordering, highlighting and pagination over ranked results."
sources: ["https://google.aip.dev/160", "https://google.aip.dev/136", "https://docs.github.com/en/rest/search/search", "https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search endpoints and query parameters

## Shape
- List with filter (AIP-160) for structured predicates on one collection:
  `GET /orders?filter=status = "PAID" AND total > 100` (URL-encode in practice).
- Separate search endpoint for free text, relevance ranking or cross-type results:
  `GET /search?q=red+shoes&type=product` or custom method `GET /products:search`.
- AIP-136: custom methods use GET to retrieve data and POST when the request could exceed URL size limits
  (so a body is needed) or has side effects. `POST /products:search` with a JSON body is therefore
  acceptable for long or structured queries; it is still a read, so document that it has no side effects.
  Query strings also land in logs.

## Parameters
| Param | Meaning |
|---|---|
| `q` | user text; document the syntax. GitHub's `q` takes keywords plus qualifiers (`QUALIFIER:value`) |
| `filter` | structured constraints, same grammar as list filters (AIP-160) |
| `order_by` | default relevance; explicit fields allowed (GitHub: `sort` and `order`, default best match) |
| `page_size`, `page_token` | cursor pagination |
| `facets` | which aggregate counts to return |

AIP-160 grammar points worth documenting if you adopt it: whitespace between bare literals is a fuzzy AND,
`OR` binds tighter than `AND` (`a AND b OR c` means `a AND (b OR c)`), `NOT` and `-` are interchangeable,
field names go on the left of a comparison, and an invalid filter returns `INVALID_ARGUMENT`.
A service may limit filter complexity but must document it.

## Responses
```json
{"results":[{"product":{...},"score":12.3,"highlights":{"title":["<em>red</em> shoes"]}}],
 "facets":{"brand":[{"value":"acme","count":42}]},
 "next_page_token":"...", "total_size_estimate": 1200}
```
- Ranked pagination: Elasticsearch cannot page past 10,000 hits with `from` and `size` by default
  (`index.max_result_window`); use `search_after` with a point in time (PIT) to page deeper
  with a stable view of the index.
- Highlighting is opt-in in GitHub's search API: the `application/vnd.github.text-match+json` media
  type adds a `text_matches` key. Whatever you choose, document the highlight format.

## Safety
- Rate-limit and cost-limit search separately. GitHub does: a dedicated search limit of 30 requests
  per minute authenticated (code search 10), 10 unauthenticated.
- Never concatenate raw user text into the engine's query language; parse or escape it.
- Apply authorization filters inside the query, not after fetching a page.

## Checked
2026-11-08. Confirmed against AIP-160, AIP-136, the GitHub REST search page and the Elasticsearch
paginate-search-results page (all read in full except GitHub, read by targeted search): filter grammar and
precedence, GET/POST rule for custom methods, GitHub search rate limits, qualifiers, `sort`/`order`,
`text-match` media type, 10,000-hit `from`/`size` limit, `search_after` and PIT. Removed unconfirmed claims:
8 KB proxy URL limit, "scores not comparable across queries", "highlights are escaped HTML", and the
`query_string`/`simple_query_string` advice. The JSON response example is illustrative, not from a vendor.
Method: documentation only; no commands were run.
