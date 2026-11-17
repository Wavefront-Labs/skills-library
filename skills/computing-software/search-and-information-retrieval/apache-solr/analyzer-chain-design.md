---
id: computing-software.search-and-information-retrieval.apache-solr.analyzer-chain-design
name: analyzer-chain-design
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [analyzers, analyzer-chain, tokenizer-filter, analysis, textfield, index-time-analysis]
level: practitioner
status: docs-checked
description: "Build Solr text analysis chains: a tokenizer plus ordered token filters in separate index and query analyzers, and when a change needs reindexing."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/analyzers.html
  - https://solr.apache.org/guide/solr/latest/indexing-guide/field-type-definitions-and-properties.html
  - https://solr.apache.org/guide/solr/latest/indexing-guide/reindexing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# analyzer-chain-design

Analysis is configured inside a `solr.TextField` (or `SortableTextField`) type. A single `<analyzer class="...">` may name one Lucene Analyzer class, but most types decompose the work into a chain: a plain `<analyzer>` with child elements naming a tokenizer and filters, in the order you want them to run.

Use `<analyzer type="index">` and `<analyzer type="query">` when the two sides differ; a single `<analyzer>` serves both phases. Analysis changes the indexed terms, not the stored value.

Query and index analysis must agree on how terms and phrases are produced, otherwise searches give unexpected results.

Reindexing: any change to the index-time chain needs it in almost all cases. A change to the query-time chain only, with separate analyzers defined, does not.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Analyzers and Reindexing pages: analyzers on `solr.TextField` or `SortableTextField`, the single-class and chain forms, `type="index"` / `type="query"` analyzers, stored values unaffected, matching index and query analysis, and the reindex rule for index-time versus query-time changes. Removed charFilter and single-tokenizer wording, the text_general example, the Admin UI Analysis screen note and `positionIncrementGap`, which the fetched pages do not state.

Method: documentation only; no commands were run.
