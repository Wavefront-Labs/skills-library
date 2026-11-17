---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.lowercase-asciifolding-filters
name: lowercase-asciifolding-filters
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, lowercase-asciifolding-filters]
level: practitioner
status: docs-checked
description: "Chain lowercase and asciifolding token filters (with preserve_original) so queries ignore case and diacritics; language-specific lowercase options."
sources:
  - https://www.elastic.co/docs/reference/text-analysis/analysis-lowercase-tokenfilter
  - https://www.elastic.co/docs/reference/text-analysis/analysis-asciifolding-tokenfilter
  - https://docs.opensearch.org/latest/analyzers/token-filters/lowercase/
  - https://docs.opensearch.org/latest/analyzers/token-filters/asciifolding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case and accent folding filters

**Goal:** match "Cafe", "café" and "CAFÉ" the same way.
- `lowercase` changes token text to lowercase (`THE Lazy DoG` becomes `the lazy dog`). Its optional `language` parameter selects Lucene's `greek`, `irish` or `turkish` lowercase filter; unset, it uses Lucene's `LowerCaseFilter`.
- `asciifolding` converts characters outside the Basic Latin block (the first 127 ASCII characters) to their ASCII equivalent if one exists, for example `à` to `a`. On `açaí à la carte` with the `standard` tokenizer it produces `acai, a, la, carte`.
- `asciifolding` has one parameter, `preserve_original` (boolean, default `false`). When `true` it emits both the folded and the original token, so accented and unaccented queries both match; the OpenSearch example with `["lowercase","custom_ascii_folding"]` emits `resume` and `résumé` at the same position.
- To set a parameter, define a custom filter of `"type":"asciifolding"` (or `"lowercase"`) under `analysis.filter` and reference it by name in the analyzer.
- Failure mode: folding loses information where the distinction between accented and unaccented characters matters in the data (OpenSearch docs warn about this).
- Both filters are also allowed in a normalizer for keyword fields (see the keyword-normalizer skill).

```
POST _analyze
{"tokenizer":"standard","filter":["lowercase","asciifolding"],"text":"CAFÉ"}
```

## Verify
- [ ] The request above returns the token `cafe`.
- [ ] With `preserve_original: true` it also returns `café` at the same position.

## Checked
2026-11-08. Confirmed against the Elasticsearch lowercase and ASCII folding token filter pages and the OpenSearch lowercase and asciifolding token filter pages: behaviour, Basic Latin scope, `preserve_original` and its default, `language` values, custom-filter pattern, the information-loss warning.
Removed: the ICU plugin claims (`icu_folding`, `analysis-icu` on every node, shard allocation failure; not on the pages read), the filter-order advice and the stop-filter sentence, and the Lucene documentation root source.
Method: documentation only; no commands were run.
