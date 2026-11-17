---
id: computing-software.search-and-information-retrieval.apache-solr.highlighting-unified
name: highlighting-unified
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [highlighting, unified-highlighter, hl-fl, snippets, fastvector]
level: practitioner
status: docs-checked
description: "Highlight Solr search results with hl=true: hl.fl stored fields, unified, original and fastVector methods, hl.q, requireFieldMatch, snippets, fragsize, tag.pre and tag.post."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/highlighting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# highlighting-unified

Highlighting needs a `uniqueKey` and stored fields. Turn it on with `hl=true` and normally set `hl.fl` (default is the `df` value; `*` globs work but then add `hl.requireFieldMatch=true`). Many parameters accept per-field overrides such as `f.title_txt.hl.snippets`.

`hl.method` (default `unified`): `unified`, `original`, `fastVector`. Unified is the newest, most accurate and performant, true to what the Lucene query matches, and recommended first. Reasons not to: passage scoring ignores query boosts, and passage breaking is less flexible.

Common parameters: `hl.q` and `hl.qparser` (highlight with a different query), `hl.snippets`, `hl.fragsize`, `hl.tag.pre`, `hl.tag.post`, `hl.encoder`, `hl.maxAnalyzedChars`, `hl.usePhraseHighlighter`, `hl.highlightMultiTerm`, `hl.defaultSummary`, `hl.alternateField`.

Field analysis should be compatible with the query; otherwise adjust `hl.q`. Example for eDisMax: `hl.q={!edismax qf=$hl.fl v=$q}&hl.qparser=lucene&hl.requireFieldMatch=true`.

Unified highlighter can speed large documents if the index stores more offset information (`hl.offsetSource`).

## Checked

2026-11-04. Confirmed against the Highlighting page: `hl.fl` default and wildcard advice, per-field overrides, unified highlighter strengths and drawbacks, `hl.q` eDisMax example, common parameters. Nothing removed.

Method: documentation only; no commands were run.
