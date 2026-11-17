---
id: computing-software.search-and-information-retrieval.apache-solr.suggester-component
name: suggester-component
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [suggester, autosuggest, suggestcomponent, lookupimpl, typeahead]
level: practitioner
status: docs-checked
description: "Build Solr autosuggest with SuggestComponent: pick a lookupImpl and dictionaryImpl, build the suggester, and query with suggest.q, suggest.dictionary and suggest.count."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/suggester.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# suggester-component

Declare `solr.SuggestComponent` in `solrconfig.xml` with one or more named `suggester` blocks: `name`, `lookupImpl` (default `FSTLookupFactory`), `dictionaryImpl` (for example `DocumentDictionaryFactory`), `field`, and often a weight field. Then attach it to a request handler such as `/suggest`; the techproducts config already has one.

Lookups named in the guide: `AnalyzingLookupFactory` (needs `suggestAnalyzerFieldType`), `FuzzyLookupFactory`, `AnalyzingInfixLookupFactory`, `BlendedInfixLookupFactory` (can build in your own path), and `FSTLookupFactory` (automaton; slower to build, lowest memory).

Building: set `buildOnCommit` or `buildOnOptimize`, or build on demand with `suggest.build=true`. The guide recommends leaving build-on-commit false and building manually or infrequently, since frequent soft commits make rebuilds costly.

Query parameters: `suggest=true`, `suggest.q`, `suggest.dictionary` (required name), `suggest.count`, `suggest.cfq` (context filter), `suggest.reload`.

It is distributed-capable and independent of spell checking.

## Checked

2026-11-04. Confirmed against the Suggester page: component and suggester parameters, lookup implementations, build options and the advice to build manually, query parameters, distributed support. Nothing removed.

Method: documentation only; no commands were run.
