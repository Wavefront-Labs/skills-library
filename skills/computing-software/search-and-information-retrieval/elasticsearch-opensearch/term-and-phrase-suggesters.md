---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.term-and-phrase-suggesters
name: term-and-phrase-suggesters
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, term-and-phrase-suggesters]
level: advanced
status: docs-checked
description: "Correct misspellings in Elasticsearch with term and phrase suggesters, a shingle sub-field for n-gram statistics, and collate to prune dead suggestions."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/search-suggesters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Did-you-mean with term and phrase suggesters (Elasticsearch)

**Goal:** "did you mean" corrections.
- Put `suggest` in a `_search` body (alone, or beside a `query`). Each named suggestion has `text` (or one global `suggest.text`) and a `term` or `phrase` object with a `field`.
- Term suggester: edit-distance candidates per analyzed token of the suggest text; it ignores the request's query. `suggest_mode`: `missing` (default, only terms not in the index), `popular` (only terms in more docs than the original), `always`. `sort`: `score` or `frequency`; `size` is per token. `analyzer` defaults to the search analyzer of the field.
- Phrase suggester: adds n-gram language-model scoring on top, choosing whole corrected phrases. It needs a mapping up front: a sub-field with a custom analyzer of `standard` tokenizer, `lowercase` and a `shingle` filter (`min_shingle_size` 2, `max_shingle_size` 3). Query `{"suggest":{"text":"noble prize","p":{"phrase":{"field":"title.trigram","gram_size":3,"direct_generator":[{"field":"title.trigram","suggest_mode":"always"}],"highlight":{"pre_tag":"<em>","post_tag":"</em>"}}}}}`.
- `gram_size` is detected from the shingle filter's `max_shingle_size` if unset. `max_errors` default 1.0 (at most one misspelled term); keep it low (1 or 2) or suggest time can exceed query time. `confidence` default 1.0 (candidates must beat the input phrase). `size` of the phrase suggester (candidates per term) defaults to 5; 3 or 5 typically works well.
- `collate` runs a templated query once per suggestion (`{{suggestion}}` holds the phrase; extra `params` allowed) on the local shard only. With `prune: true` every suggestion is returned with a `collate_match` flag; default `prune` is false.
- Direct generator options: `max_edits` (1 or 2, default 2), `prefix_length` (default 1), `min_word_length` (default 4), `max_term_freq` (default 0.01), `min_doc_freq`. Only `direct_generator` exists. Add a second generator on a reversed-token sub-field with `pre_filter` and `post_filter` of `reverse` to get around the fixed-prefix requirement.
- Smoothing: `stupid_backoff` (default, discount 0.4), `laplace` (alpha 0.5), `linear_interpolation` (all lambdas required).
- Suggesting across indices with different analysis chains is not supported.
- `?typed_keys` prefixes response names with the suggester type.
- Failure mode: suggesting from a noisy field proposes misspellings (not stated on the page; a judgment).
- OpenSearch: not checked; its did-you-mean page was not used for these claims.

## Verify
- [ ] On the page's example data, `noble prize` returns `nobel prize` with a `highlighted` form.

## Checked
Checked 2026-11-08 against the Elasticsearch "Suggester examples" page. Only Elasticsearch was checked. Removed: the placeholder `quik brwn` example, which the page does not support, and the generic cross-version notes.
Method: documentation only; no commands were run.
