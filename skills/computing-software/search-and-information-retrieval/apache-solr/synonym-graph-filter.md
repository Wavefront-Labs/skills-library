---
id: computing-software.search-and-information-retrieval.apache-solr.synonym-graph-filter
name: synonym-graph-filter
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [synonyms, synonym-graph, flatten-graph, multi-word-synonyms, synonymgraphfilterfactory]
level: advanced
status: docs-checked
description: "Configure SynonymGraphFilterFactory in Solr: the synonyms file formats, expand, ignoreCase, why to apply it at query time, and the Flatten Graph requirement at index time."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/filters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# synonym-graph-filter

`solr.SynonymGraphFilterFactory` maps single- or multi-token synonyms and produces a correct token graph. It replaces the older Synonym Filter, which gives incorrect graphs for multi-token synonyms.

Placement:
- Preferred at query time for correct positional queries.
- If used at index time, follow it with `solr.FlattenGraphFilterFactory`, because the indexer cannot consume a graph.
- It cannot consume an input graph correctly, so avoid chaining it after another graph-producing filter.

Arguments:
- `synonyms` (required): file path(s), comma separated. Blank lines and `#` lines are ignored.
- Two rule forms: `a,b,c` (any match is replaced by all, including the original) or `a,b => c,d` (left replaced by right; original dropped unless also on the right).
- `ignoreCase` (default false), `expand` (default true; false reduces to the first entry).
- `format` (`solr` default, or `wordnet`), `tokenizerFactory` (default Whitespace).

On the standard query parsers keep `sow=false` (the default) so multi-word synonyms can match.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Filters page (Synonym Graph Filter) and the standard and eDisMax parser pages for the `sow` default: replacement for the Synonym Filter, Flatten Graph at index time, query-time preference, the input-graph limitation, `synonyms`, both rule forms, `ignoreCase`, `expand`, `format` and `tokenizerFactory` defaults. Nothing removed.

Method: documentation only; no commands were run.
