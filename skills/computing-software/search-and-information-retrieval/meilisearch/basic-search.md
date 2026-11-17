---
id: computing-software.search-and-information-retrieval.meilisearch.basic-search
name: basic-search
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [basic-search, search-response, estimated-total-hits, meilisearch]
level: intro
status: docs-checked
description: "Run a first Meilisearch full-text query with q, read the hits response fields, rely on typo handling and multi-word ranking, and page with limit and offset."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/getting_started/basic_search"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic search in Meilisearch

A search is a POST to `/indexes/<index>/search` with a JSON body whose `q` holds the user's text, sent with an `Authorization: Bearer <API_KEY>` header. Example body: `{"q": "galaxy"}`.

## Reading the response

- `hits`: matching documents ordered by relevance.
- `query`: the text you sent.
- `processingTimeMs`: how long the search took.
- `limit`: maximum hits returned, default 20.
- `offset`: hits skipped, used for paging.
- `estimatedTotalHits`: estimated number of matching documents (an estimate, not an exact count).

## Behaviour to rely on

- Typos are tolerated automatically, so `galxy` or `galaxi` still finds "galaxy" (see typo tolerance settings).
- With several words, documents containing all of them rank above those containing only some, for example `dark knight`. The `matchingStrategy` parameter changes how terms are dropped.
- `limit` and `offset` page through results: `{"q": "action", "limit": 5, "offset": 10}` returns five hits starting at the eleventh match.

## Next features

Highlighting, phrase search with quotes, filters and sorting, and relevancy tuning all build on this same endpoint; add them as extra keys in the request body.

## Checked

2026-11-03. Confirmed claim by claim against the Basic search page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
