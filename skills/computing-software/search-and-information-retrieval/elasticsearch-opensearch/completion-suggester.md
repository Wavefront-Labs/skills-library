---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.completion-suggester
name: completion-suggester
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, completion-suggester, es-suggesters]
level: advanced
status: docs-checked
description: "Fast prefix autocomplete using a completion field held in memory, with fuzzy options and contexts."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Completion suggester

**Goal:** type-ahead from a curated list.
- Mapping `"suggest":{"type":"completion"}`; index `{"suggest":{"input":["fox","foxes"],"weight":10}}`.
- Query: `{"suggest":{"s":{"prefix":"fo","completion":{"field":"suggest","size":5,"skip_duplicates":true}}}}`.
- Fuzzy queries (`fuzzy: {}` or `fuzzy: true` for defaults) tolerate typos; regex prefixes are also supported.
- `contexts` (types `category` and `geo`) filter or boost suggestions; once a field has context mappings, a context is mandatory at index and query time. At most 10 context mappings per completion field.
- It is built for speed with data structures that are costly to build and stored in memory. Suggestions are near real-time (visible after a refresh) and deleted documents are never shown. It is not for spell correction; use the term or phrase suggesters for that.
- `weight` is an optional positive integer that ranks suggestions; the shorthand input form cannot carry a weight. A single input is capped at `max_input_length`, default 50 UTF-16 code points (index time).
- Failure mode: very many or very long suggestion inputs make the in-memory structure big.

## Verify
- [ ] Prefix "fo" returns "fox" with the weight order respected.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited page is the Elasticsearch suggesters page; OpenSearch was not checked here.

## Checked
2026-11-08. Read the Elasticsearch Suggesters page (completion section): mapping, input and weight, `skip_duplicates`, fuzzy, regex, contexts and the limit of 10 context mappings, in-memory structure, near-real-time behaviour. Corrected the claim that suggestions ignore deletions until merged (the page says deleted documents are never shown) and removed "no full-text scoring" (not stated).
Method: documentation only; no commands were run.
