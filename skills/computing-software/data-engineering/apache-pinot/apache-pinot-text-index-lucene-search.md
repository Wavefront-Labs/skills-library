---
id: computing-software.data-engineering.apache-pinot.apache-pinot-text-index-lucene-search
name: apache-pinot-text-index-lucene-search
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, text-index, text-match, lucene, parser, allowleadingwildcard, defaultoperator, enableprefixmatch, slop, inorder, matchphrase]
level: advanced
status: docs-checked
description: "Lucene text index on RAW STRING columns: TEXT_MATCH usage, parser and query options (CLASSIC, STANDARD, COMPLEX, MATCHPHRASE, slop, inOrder) and index-property tuning keys."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/text-search-support.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lucene text index and TEXT_MATCH

The text index is built on Lucene and is supported only on RAW columns, not dictionary-encoded ones. The docs recommend it over the experimental native text index. Enable it in `fieldConfigList` and also list the column in `noDictionaryColumns`:
```
"fieldConfigList":[{ "name":"text_col_1", "encodingType":"RAW", "indexTypes":["TEXT"] }],
"tableIndexConfig": { "noDictionaryColumns": ["text_col_1"] }
```
Stop words: a built-in English list is ignored at index and search time. Customise per column with `properties` in the field config: `stopWordInclude` and `stopWordExclude` (comma-separated), for example excluding `it` so it is searchable.

Query: `TEXT_MATCH(text_column_name, search_expression [, options])`, for example `WHERE TEXT_MATCH(body, '"machine learning" AND gpu')`. Phrases go in double quotes; `stream*` and regex forms such as `/.*Exception/` are shown in the docs. TEXT_MATCH can also appear in SELECT and ORDER BY.

Options (third argument string, such as `'parser=MATCHPHRASE,enablePrefixMatch=true,slop=1'`):
- `parser`: `CLASSIC` (default), `STANDARD`, `COMPLEX`, `MATCHPHRASE`.
- `allowLeadingWildcard`: default false.
- `defaultOperator`: `AND` or `OR`; default OR.
- With `parser=MATCHPHRASE` only: `enablePrefixMatch` (last term as prefix, default false), `slop` (non-negative, default 0) and `inOrder` (default true).

Index properties in the docs' parameter table include `queryCache` (default false), `useANDForMultiTermQueries` (false), `luceneUseCompoundFile` (true), `luceneMaxBufferSizeMB` (500), `luceneAnalyzerClass` (StandardAnalyzer), `luceneQueryParserClass`, `enablePrefixSuffixMatchingInPhraseQueries` (false), `reuseMutableIndex` (false), `docIdTranslatorMode` (Default, TryOptimize or Skip) and `caseSensitive` (false). The compound-file and buffer-size settings can speed index writing at the cost of file descriptors or memory. Raise `pinot.lucene.max.clause.count` at cluster level if Lucene throws TooManyClauses.

Multi-column text index (introduced in Pinot 1.4.0): one `tableIndexConfig.multiColumnTextIndexConfig` per table with `columns` (required), shared `properties` and `perColumnProperties` overrides. A column may be in either a per-column text index or the multi-column config, not both. Per the docs it queries faster and uses less disk, but rebuilds from scratch. Newly built TEXT indexes under the 1.4.0 doc-id behaviour need Pinot 1.4.0 or later readers.

## Checked

Confirmed against the Pinot docs page "Text search support": RAW-only restriction, parser and option values and defaults, property table defaults, multi-column config shape and 1.4.0 introduction. Removed the unsourced claims that the native text index was removed in 1.5.0 and that leading wildcards are expensive, and replaced the property list with ones the page tabulates.

Method: docs-only read of cited pages, 2026-11-08
