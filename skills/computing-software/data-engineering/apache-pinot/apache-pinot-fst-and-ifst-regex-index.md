---
id: computing-software.data-engineering.apache-pinot.apache-pinot-fst-and-ifst-regex-index
name: apache-pinot-fst-and-ifst-regex-index
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, fst-index, ifst, regexp-like, lucene-fst, indexes-ifst, like, text-pattern-matching]
level: advanced
status: docs-checked
description: "FST index for case-sensitive REGEXP_LIKE on dictionary-backed STRING columns, the case-insensitive IFST variant, and restrictions."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/fst-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FST and IFST regex indexes

The FST (Finite State Transducer) index is built over dictionary values and accelerates regex queries on STRING columns.

```
{ "name": "city", "encodingType": "DICTIONARY", "indexType": "FST" }
```
(in `fieldConfigList`). It creates one file, `.lucene.fst`.

Supported columns: STRING only, single-valued, with dictionary values available: either a dictionary-encoded forward index, or a standalone dictionary with a RAW forward index (`"encodingType": "RAW", "indexTypes": ["FST"], "indexes": { "dictionary": {} }`). Do not keep the column in legacy `tableIndexConfig.noDictionaryColumns` or `noDictionaryConfig`; Pinot rejects the config.

Limitations:
- Only case-sensitive `REGEXP_LIKE` predicates can use FST. Pinot's `LIKE` is case-insensitive and is rewritten to `REGEXP_LIKE` with the `'i'` flag, which cannot use FST; without IFST it falls back to dictionary or scan evaluation. Enabling FST does not change which rows `LIKE` matches.
- Only stored or completed segments, not consuming segments of real-time tables.
- Works best for prefix patterns; suffix-only or infix-only patterns may not benefit as much.
- If an inverted index is also enabled on the column, FST can use it for faster lookups.
- For tokenized full-text search use the text index instead.

**IFST** (case-insensitive FST): enable with
```
{ "name": "notes", "encodingType": "DICTIONARY", "indexes": { "ifst": { "enabled": true } } }
```
It creates `.lucene.ifst`, supports `LIKE` and `REGEXP_LIKE` with the `'i'` flag (for example `notes LIKE 'Us%'` or `REGEXP_LIKE(notes, '^Us', 'i')`), has the same segment and column restrictions, and also works best for prefix queries.

## Checked

2026-11-08. Read the whole pinot-docs fst-index page. Confirmed column rules, file names, case sensitivity, the LIKE rewrite, IFST config, the RAW plus dictionary form and the legacy noDictionary conflict. Removed the unsourced cardinality advice and the leading-wildcard gotcha, replaced with the documented prefix-pattern note.

Method: documentation only; no commands were run.
