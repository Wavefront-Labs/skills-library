---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.synonym-graph-filter
name: synonym-graph-filter
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, synonym-graph-filter]
level: advanced
status: docs-checked
description: "Apply synonym_graph in a search analyzer with inline synonyms, a synonyms_path file or a synonyms_set; rule formats, expand, lenient and stop-filter interplay."
sources:
  - https://www.elastic.co/docs/reference/text-analysis/analysis-synonym-graph-tokenfilter
  - https://docs.opensearch.org/latest/analyzers/token-filters/synonym-graph/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synonym graph filter at search time

**Goal:** expand queries with multi-word synonyms without reindexing every change.
```
"filter":{"syn":{"type":"synonym_graph","synonyms":["tv, television","laptop, notebook"]}}
"analyzer":{"search_syn":{"type":"custom","tokenizer":"standard","filter":["lowercase","syn"]}}
```
- Use `synonym_graph` in a search analyzer only (both products). OpenSearch explains why: at index time it ignores `positionLength`, so a multi-word synonym shifts later positions and can break `match_phrase`. For index time use the plain `synonym` filter.
- Rules (Solr format by default; `format: wordnet` in OpenSearch): equivalent `a, b, c` and explicit `a => b`.
- Sources: inline `synonyms`; `synonyms_path` (relative to the config directory, file must exist on every node); Elasticsearch also `synonyms_set` (one name or an array, up to 100 sets per filter, 100,000 rules per set by default via `synonyms.max_synonym_rules`).
- `expand` (default true): `quick, fast` becomes quick/fast in both directions; false maps everything to the first term. It does not affect `=>` rules.
- `lenient`: Elasticsearch defaults it to the value of `updateable` (false by default); OpenSearch defaults to false. With false, an unparseable rule fails the analyzer or index creation; with true, only the bad rule or term is skipped.
- Order matters: filters before `synonym_graph` also process the rules (for example a stemmer stems the rules; a preceding `stop` removes stop words from rules, and with `lenient` false the request is rejected). `word_delimiter_graph`, `ngram`, `edge_ngram`, `shingle`, `multiplexer` before it cause errors (OpenSearch lists these; Elasticsearch lists multiplexer, word_delimiter_graph, ngram). OpenSearch offers `synonym_analyzer` to parse rules with a different analyzer.
- A `stop` filter after `synonym_graph` removes the expanded terms, so a rule whose target is a stop word no longer matches.
- Elasticsearch: a `synonyms_set` must exist before an index references it, or the index is left partially created and inoperable. A circuit breaker (95% heap by default) guards the synonym map build.
- Rules can change without reindexing; reload via the reload search analyzers API (see `reload-search-analyzers-and-synonym-sets`).

## Verify
- [ ] `_analyze` with `search_syn` on "tv" outputs both `tv` and `television`.

## Checked
Checked 2026-11-08 against the Elasticsearch page "Synonym graph token filter" and the OpenSearch page "Synonym graph token filter" (both read in full). Removed: the claim that "syntax errors in a rule reject the analyzer on creation" as stated (behaviour depends on `lenient`; the pages describe the stop-word case), and the unqualified claim that index-time use is "not supported" (the pages say it is meant for search analyzers only and explain the position problem).
Method: documentation only; no commands were run.
