---
id: computing-software.search-and-information-retrieval.apache-solr.spellcheck-component
name: spellcheck-component
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [spellcheck, collation, did-you-mean, directsolrspellchecker, spellcheck-component]
level: practitioner
status: docs-checked
description: "Add did-you-mean to Solr with the SpellCheckComponent: DirectSolrSpellChecker, IndexBasedSpellChecker, spellcheck.q, count, collate, maxCollations and buildOnCommit."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/spell-checking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spellcheck-component

Configure a `solr.SpellCheckComponent` in `solrconfig.xml` with one or more dictionaries.

Implementations:
- `DirectSolrSpellChecker`: uses terms straight from the main index, no parallel index to build.
- `IndexBasedSpellChecker`: builds a parallel index from a field (often a copy of title, body and so on). Options include `buildOnCommit` and `buildOnOptimize`; avoid building on every commit if commits are frequent. The default distance measure is Levenshtein.
- File-based and word-break checkers also exist.

Request parameters: `spellcheck=true`, `spellcheck.q` (else `q` is used), `spellcheck.dictionary` (repeatable), `spellcheck.count` (default 1; set without a value means 5), `spellcheck.onlyMorePopular`, `spellcheck.maxResultsForSuggest` (suggest when results are at or below this number), `spellcheck.extendedResults`, `spellcheck.build`, `spellcheck.reload`.

Collation: `spellcheck.collate`, `spellcheck.maxCollations`, `spellcheck.maxCollationTries` (test collations against the index), `spellcheck.collateExtendedResults`.

## Checked

2026-11-04. Confirmed against the Spell Checking page: spellchecker implementations, `buildOnCommit` and `buildOnOptimize`, Levenshtein default for index-based checkers, `spellcheck.count` defaults (1; 5 when set without a value), `spellcheck.maxResultsForSuggest`, repeatable `spellcheck.dictionary`, collation parameters. Removed a generic closing line.

Method: documentation only; no commands were run.
