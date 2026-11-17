---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.keyword-normalizer
name: keyword-normalizer
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, keyword-normalizer, es-normalizers]
level: practitioner
status: docs-checked
description: "Define a normalizer with lowercase and asciifolding filters so keyword fields match case-insensitively and aggregate on the normalized value."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/normalizer
  - https://www.elastic.co/docs/reference/text-analysis/normalizers
  - https://docs.opensearch.org/latest/analyzers/normalizers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyword normalizer for case-insensitive exact match

**Goal:** case-insensitive, accent-insensitive exact match and terms aggregations on keyword fields.
```
PUT index
{"settings":{"analysis":{"normalizer":{"my_normalizer":{"type":"custom","char_filter":[],"filter":["lowercase","asciifolding"]}}}},
 "mappings":{"properties":{"foo":{"type":"keyword","normalizer":"my_normalizer"}}}}
```
- A normalizer is like an analyzer except that it guarantees a single token. It has no tokenizer and accepts only filters that work per character, not whole-token filters such as a stemmer.
- Elasticsearch ships a built-in normalizer named `lowercase`; any other normalization needs a custom normalizer.
- The normalizer runs before indexing and at search time, both for the `match` query and for term-level queries such as `term`. In the Elasticsearch example, `BÀR` and `bar` both match a `term` query for `BAR`.
- `_source` keeps the original; a `terms` aggregation returns the normalized values (`bar`, not `BÀR`).
- Filters allowed in an Elasticsearch normalizer: arabic_normalization, asciifolding, bengali_normalization, cjk_width, decimal_digit, elision, german_normalization, hindi_normalization, indic_normalization, lowercase, pattern_replace, persian_normalization, scandinavian_folding, serbian_normalization, sorani_normalization, trim, uppercase. Char filters (for example a `mapping` char filter) go in `char_filter`.
- OpenSearch accepts only filters that are normalizing factories: the `common-analysis` module (including `truncate` and `scandinavian_normalization`) plus, from plugins in the core repository, `analysis-icu` (`icu_normalizer`, `icu_folding`, `icu_transform`) and `analysis-kuromoji` (`kuromoji_iteration_mark` char filter).
- Synthetic source (Elasticsearch): a keyword field with a normalizer stores the pre-normalized value too, so values are stored twice. The mapping parameter `normalizer_skip_store_original_value: true` avoids that; it defaults to `false` for custom normalizers and `true` for the built-in `lowercase` normalizer.

## Verify
- [ ] A `term` query for `NIKE` matches a stored `nike`.
- [ ] A `terms` aggregation on the field shows one bucket for `Nike` and `NIKE`.
- [ ] `GET <index>/_analyze` with `"normalizer":"my_normalizer"` returns the single folded token (OpenSearch docs show this check).

## Checked
2026-11-08. Confirmed against the Elasticsearch normalizer mapping parameter page and Text analysis Normalizers page, and the OpenSearch Normalizers page: single-token guarantee, no tokenizer, allowed filter lists, built-in `lowercase` normalizer, query-time and index-time application, normalized aggregation keys, `normalizer_skip_store_original_value` and its defaults, OpenSearch plugin filter lists.
Removed: the `case_insensitive: true` term-query alternative (not on the fetched pages), the claim that a tokenizing filter is rejected with an error (the docs only say such filters are not accepted), and the unconfirmed-cluster boilerplate.
Method: documentation only; no commands were run.
