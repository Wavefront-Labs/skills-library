---
id: computing-software.search-and-information-retrieval.typesense.curation-synonyms-and-stemming
name: curation-synonyms-and-stemming
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [curation-synonyms, curation-stemming, stemming-dictionary, typesense]
level: advanced
status: docs-checked
description: "Make Typesense curation rules match through synonyms with rule.synonyms true and through stemming with rule.stem true and an optional stemming_dictionary."
sources: ["https://typesense.org/docs/30.2/api/curation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synonyms and stemming in curation rules

By default a rule matches the query text literally. Two switches widen that; both default to `false`.

## Synonyms

```json
{"id": "synonyms2",
 "rule": {"query": "credit card", "match": "exact", "synonyms": true},
 "includes": [{"id": "4", "position": 1}]}
```

If the query tokens do not match any rule, Typesense tries the synonyms of the tokens. With a synonym item `{"id": "card-synonyms", "synonyms": ["credit card", "payment card", "cc"]}`, searching `payment card` or `cc` triggers the rule above.

## Stemming

```json
{"id": "stemmer2",
 "rule": {"query": "People", "match": "exact", "stem": true, "stemming_dictionary": "set1"},
 "includes": [{"id": "4", "position": 1}]}
```

`stem: true` makes the rule match stemmed forms. `stemming_dictionary` references an already added stemming dictionary (here `set1`).

Both options sit inside `rule`.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Curation page (https://typesense.org/docs/30.2/api/curation.html) and its source markdown in typesense-website (placeholder rules, sort_by and filter_by examples), plus the API Keys page for curation_sets actions. Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
