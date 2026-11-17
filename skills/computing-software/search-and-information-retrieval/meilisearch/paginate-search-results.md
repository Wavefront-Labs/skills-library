---
id: computing-software.search-and-information-retrieval.meilisearch.paginate-search-results
name: paginate-search-results
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [pagination, hits-per-page, max-total-hits, meilisearch]
level: practitioner
status: docs-checked
description: "Paginate Meilisearch results with limit/offset for previous-next UIs or hitsPerPage/page for numbered pages, and the maxTotalHits performance limit."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/paginate_search_results"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paginate search results

Meilisearch supports two pagination styles.

## Previous and Next buttons (recommended)

Use `limit` (page size) and `offset` (results skipped). The response carries `estimatedTotalHits`, a partial count, which is cheap to compute. Page offset formula: `offset = limit * (target page number - 1)`, so limit 20 and offset 40 gives the third page. To know whether a Next button should be enabled, request `limit` = page size plus one and do not display the extra hit; if you get the extra hit there is another page. Disable Previous when `offset` is 0. A response with fewer hits than `limit` is the last page.

## Numbered page selectors

Add `hitsPerPage` and/or `page` to the request. The response then replaces `estimatedTotalHits` with exhaustive `totalHits` and `totalPages`, and returns the current `page`. For 100 results and `hitsPerPage` 25 there are four pages. These parameters take precedence: any `offset` and `limit` in the same query are ignored.

Warnings: exhaustive counting is resource-intensive, and switching styles changes the response shape, so a frontend relying on `estimatedTotalHits` can break.

## maxTotalHits

Meilisearch returns a limited maximum number of results per query, set with the `maxTotalHits` pagination index setting. Raising it above the default hurts performance; values over 20000 may make queries take seconds.

## Checked

2026-11-03. Confirmed claim by claim against the Paginate search results page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
