---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.stemming-and-stopwords
name: stemming-and-stopwords
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, stemming, stop-words, keyword-marker]
level: practitioner
status: docs-checked
description: "Use language analyzers, the stemmer, porter_stem and stop filters, stem_exclusion and keyword_marker to protect terms, with the filter-order rules."
sources:
  - https://www.elastic.co/docs/reference/text-analysis/analysis-lang-analyzer
  - https://www.elastic.co/docs/reference/text-analysis/analysis-stemmer-tokenfilter
  - https://www.elastic.co/docs/reference/text-analysis/analysis-stop-tokenfilter
  - https://www.elastic.co/docs/reference/text-analysis/analysis-keyword-marker-tokenfilter
  - https://www.elastic.co/docs/reference/text-analysis/analysis-porterstem-tokenfilter
  - https://docs.opensearch.org/latest/analyzers/token-filters/stemmer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stemming and stop words

**Goal:** match inflected forms (run, running) without destroying exact terms.
- Built-in language analyzers (for example `english`) bundle stop words and a stemmer. The `english` analyzer can be rebuilt as a custom analyzer: tokenizer `standard`, then `possessive_english` stemmer, `lowercase`, `stop` (`_english_`), `keyword_marker`, `stemmer` (`english`).
- `stem_exclusion` (array of lowercase words) on a language analyzer is implemented as a `keyword_marker` filter. Stop words can be overridden with `stopwords` or `stopwords_path`.
- Custom: `"filter":["lowercase","stop","stemmer"]`. The `stemmer` filter defaults to `language: english` (porter); `name` is an alias for `language` (Elasticsearch says `language` wins if both are set; OpenSearch says `name` is ignored). Example `{"type":"stemmer","language":"light_german"}`.
- English variants documented for the Elasticsearch stemmer: `english`, `light_english`, `minimal_english`, `porter2`, `possessive_english` (`lovins` is deprecated since 8.16.0). Other languages have their own values (for example `light_french`, `spanish`); take the exact name from the stemmer page.
- `porter_stem` is equivalent to the `stemmer` filter's english variant, stems more aggressively than kstem, and needs lowercase tokens: put `lowercase` before it.
- Protect terms with `keyword_marker` (`keywords`, `keywords_path` or `keywords_pattern`, plus `ignore_case`); it must be listed before any stemmer. Poorly written `keywords_pattern` regexes can slow or crash a node.
- The `stop` filter defaults to the English list (a, an, and, are, as, at, be, but, by, for, if, in, into, is, it, no, not, of, on, or, such, that, the, their, then, there, these, they, this, to, was, will, with). Options: `stopwords` (language value like `_german_`, an array, or `_none_`), `stopwords_path`, `ignore_case` (default false), `remove_trailing` (default true; set false with a completion suggester).
- Stop word lists and stemmers are language specific: confirm the analyzer or filter name for your language.

## Verify
- [ ] `_analyze` with `tokenizer: whitespace` and filters `[keyword_marker(keywords: ["jumping"]), stemmer]` on "fox running and jumping" returns fox, run, and, jumping (this is the page's example).

## Checked
Checked 2026-11-08 against the Elasticsearch pages "Language analyzers", "Stemmer token filter", "Stop token filter", "Keyword marker token filter" and "Porter stem token filter", and the OpenSearch "Stemmer token filter" page. The OpenSearch keyword_marker page was fetched but the stemmer, stop and analyzer details above are Elasticsearch statements. Removed because not on the pages: the "to be or not to be" phrase-query warning, the over-stemming warning, and the `running shoes` verify example.
Method: documentation only; no commands were run.
