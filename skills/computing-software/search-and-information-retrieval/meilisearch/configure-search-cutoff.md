---
id: computing-software.search-and-information-retrieval.meilisearch.configure-search-cutoff
name: configure-search-cutoff
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [search-cutoff, search-cutoff-ms, response-time, meilisearch]
level: advanced
status: docs-checked
description: "Bound Meilisearch query time with searchCutoffMs, including the 1500 ms internal default, risks of low values and the effect on remote embedders."
sources: ["https://www.meilisearch.com/docs/capabilities/full_text_search/how_to/configure_search_cutoff"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure the search cutoff

`searchCutoffMs` is the maximum time Meilisearch spends on one query. When reached, it stops and returns the best results found so far, correctly ranked but possibly incomplete.

## Defaults

The setting defaults to `null`; in that state Meilisearch interrupts searches after 1500 milliseconds. Setting an integer replaces that limit, for example 150. You can get, update or reset it through the settings endpoint.

## Choosing a value

- Too low can yield incomplete or even empty results on broad queries. The docs suggest starting between 100 and 500 ms, and generally not going below 500 ms; it is a safety net, including against crafted slow queries, not a tuning knob.
- If searches are slow in general, instead restrict searchable attributes, add stop words, or disable prefix search.

## Remote embedders

For indexes with an embedder that calls an external API at search time, the embedding request timeout is derived from `searchCutoffMs`. A 150 ms cutoff suits lexical search but usually not a hosted embedding API. If the embedder is too slow the query loses semantic results, and a pure semantic search can fail with HTTP 500. Raise the cutoff first when this happens. Local embedders are unaffected.

## Checked

2026-11-03. Confirmed claim by claim against the Configure search cutoff page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
