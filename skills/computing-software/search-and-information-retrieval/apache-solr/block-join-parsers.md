---
id: computing-software.search-and-information-retrieval.apache-solr.block-join-parsers
name: block-join-parsers
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [block-join, parent-child-query, child-parser, parent-parser, nested-query]
level: advanced
status: docs-checked
description: "Query nested Solr documents with the block join parsers {!parent} and {!child}: parentPath, childPath, the of block mask, filters and excludeTags, and the [child] transformer."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/block-join-query-parser.html
  - https://solr.apache.org/guide/solr/latest/query-guide/searching-nested-documents.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# block-join-parsers

Block join parsers search relations indexed as nested documents.

With a `_nest_path_` field:
- `q={!parent parentPath="/"}pages_i:1` returns parents of children matching the sub-query.
- `q={!parent parentPath="/skus" childPath="manuals"}pages_i:1` limits the levels.
- `q={!child parentPath="/"}description_t:staplers` returns children of matching parents; add `childPath="skus"` to pick a level.

Without `_nest_path_`, give the parser a block mask: `{!child of="content_type:parent"}title:lucene`, and `which` for the parent parser. The mask must select exactly the parent documents; a child clause that matches parent documents causes wrong results. `{!child of=<mask>}` is equivalent to `*:* -<mask>` constrained to children of matches.

`{!child}` also takes `filters` and `excludeTags` local params. Combine required clauses with `+`, for example `+<parents> +BRAND:Foo`.

Attach children to results with the `[child]` transformer (`childFilter`); it needs `_nest_path_` to rebuild structure, otherwise returns a flat list.


## Checked

2026-11-04. Confirmed against the Solr Reference Guide Block Join Query Parser and Searching Nested Documents pages: `parentPath`/`childPath` with `_nest_path_`, the `of` and `which` block masks, `filters` and `excludeTags`, the equivalence to `*:* -<mask>`, and `[child]` with `childFilter`. Removed `limit` for the transformer and the closing speed claim, which these pages do not state.

Method: documentation only; no commands were run.
