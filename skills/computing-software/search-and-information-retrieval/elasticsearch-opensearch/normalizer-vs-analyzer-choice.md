---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.normalizer-vs-analyzer-choice
name: normalizer-vs-analyzer-choice
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, normalizer-vs-analyzer-choice]
level: advanced
status: docs-checked
description: "Decide between a normalizer on keyword and an analyzer on text for identifiers, tags, sort keys and facets, and use multi-fields when you need both."
sources:
  - https://www.elastic.co/docs/reference/text-analysis/normalizers
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/normalizer
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/multi-fields
  - https://docs.opensearch.org/latest/analyzers/normalizers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose a normalizer or an analyzer

**Goal:** the cheapest correct field design.
- Needs whole-value matching, sorting, facets: `keyword` field with a `normalizer`. The normalizer guarantees a single token and only allows per-character filters (no stemming, no synonyms).
- Needs word-level matching: `text` field with an analyzer (which has a tokenizer and can emit many tokens).
- Need both: a `text` field with a `keyword` sub-field under `fields`, and put the `normalizer` on the keyword sub-field. A multi-field mapping is separate from the parent's: it inherits no options, and `_source` is unchanged.
- A normalizer on a keyword field is applied at index time and at search time (`match` and term-level queries), so `Naïve` finds an indexed `naive` when the normalizer holds `asciifolding` and `lowercase` (OpenSearch docs example).
- Aggregations return the normalized form, not the original casing, because values are converted before indexing.
- Adding a multi-field to an existing field is possible with the update mapping API, but existing documents get no value for it until populated with the update by query API. Changing the normalizer on an existing field is not covered by the documentation read here: plan a new index and reindex, and test it.

## Verify
- [ ] Sorting on the normalized sub-field gives case-insensitive ordering.
- [ ] A `terms` aggregation returns one bucket for `Nike` and `NIKE`.

## Checked
2026-11-08. Confirmed against the Elasticsearch Normalizers, normalizer mapping parameter and multi-fields pages and the OpenSearch Normalizers page: single-token rule, per-character filters only, index-time and query-time application, normalized aggregation keys, multi-field independence from the parent, adding multi-fields via update mapping and the need to populate them with update by query.
Removed: the definite claim that a normalizer cannot be added in place (not stated on the pages read) and the `GET <index>/_mapping/field/<name>` hint.
Method: documentation only; no commands were run.
