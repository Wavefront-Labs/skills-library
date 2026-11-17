---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.multi-match-query
name: multi-match-query
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, multi-match-query]
level: practitioner
status: docs-checked
description: "Search several fields with multi_match types best_fields, most_fields, cross_fields and phrase_prefix, with per-field boosts."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-multi-match-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-match across fields

**Goal:** one box searching title, body and tags with sensible scoring.
```
{"query":{"multi_match":{"query":"red shoes","fields":["title^3","body","tags"],"type":"best_fields","tie_breaker":0.3}}}
```
- Per-field boost uses the caret (`title^3`).
- `best_fields` (default) finds documents matching any field and uses the `_score` of the best field; it builds a `match` query per field wrapped in `dis_max`. With `tie_breaker`, the score is the best field plus `tie_breaker * _score` of every other matching field.
- `most_fields` combines the scores of all matching fields; suited to the same text analysed in different ways (synonyms, stemming, shingles).
- `cross_fields` treats fields with the same `analyzer` as one big field and looks for each word in any field (for example `first_name` and `last_name`). Fields with different analyzers are grouped by analyzer; it is mainly useful on short fields with a `boost` of `1`.
- `phrase` and `phrase_prefix` run `match_phrase` / `match_phrase_prefix` per field and use the best score; `bool_prefix` runs `match_bool_prefix` per field and combines scores. `fuzziness` cannot be used with `phrase` or `phrase_prefix`.
- `best_fields` and `most_fields` apply `operator` and `minimum_should_match` per field, not per term; `cross_fields` (or `combined_fields`) works per term.

## Verify
- [ ] Compare ranking for `best_fields` and `most_fields` on a sample query and a few documents.

## Scope
The Elasticsearch reference page was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference Multi-match query page. Confirmed: each type's behaviour, `tie_breaker` formula, caret boosts, per-field operator handling, `cross_fields` analyzer grouping, the `fuzziness` restriction. Removed: "supports typeahead" (not stated) and the `explain=true` check, and the OpenSearch source root.

Method: documentation only; no commands were run.
