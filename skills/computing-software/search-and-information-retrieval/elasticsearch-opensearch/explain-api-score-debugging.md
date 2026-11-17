---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.explain-api-score-debugging
name: explain-api-score-debugging
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, explain-api-score-debugging, es-explain-profile]
level: practitioner
status: docs-checked
description: "Use the explain API and explain=true to see the score tree and why a given document matches or not."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-explain
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explain why a document did or did not match

**Goal:** answer "why is this ranked here" with evidence.
- Per document: `GET my-index/_explain/1 {"query":{"match":{"title":"fox"}}}` (POST also works). Exactly one index name and a document id; needs the `read` index privilege.
- The response has `matched` (boolean) and a nested `explanation` with `value`, `description` and `details`.
- Per search: add `"explain": true` (body property, or the `explain` query parameter) to get score-computation detail on every hit; default is false.
- The example tree breaks a match score into boost, IDF and term frequency, each with its inputs.
- Combine with `POST my-index/_analyze` to see why terms do not meet.
- The explain API also accepts `q` (Lucene query string) as a query parameter instead of a body, plus `routing`, `preference` and `_source`.
- Failure mode: `explain` output is large; use it with small `size`.

## Verify
- [ ] `matched` is true for a document you expect to match, and `explanation.value` is the score for it.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch explain API reference in full; the search API reference was read for the explain parameter only (first 100000 characters). OpenSearch was not checked.
