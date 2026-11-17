---
id: computing-software.search-and-information-retrieval.apache-solr.standard-parser-syntax
name: standard-parser-syntax
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [standard-parser, standard-query-parser, lucene-syntax, wildcard-query, fuzzy-search, range-query]
level: intro
status: docs-checked
description: "Write queries for the Solr standard (lucene) query parser: fielded terms, phrases, wildcards, fuzzy ~, proximity, ranges, boosts, field:*, boolean operators, q.op, df, sow."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/standard-query-parser.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# standard-parser-syntax

The standard parser is the default (`defType=lucene`). Parameters: `q`, `q.op` (AND or OR), `df` default field, `sow`, `fl`, `debug`.

Syntax:
- Terms and quoted phrases; `field:term` targets a field.
- Wildcards `?` (one char) and `*` (zero or more) inside single terms, not phrases.
- Fuzzy: `roam~` or `roam~1`; edit distance 0 to 2, default 2. For prefixLength or maxExpansions use the fuzzy parser.
- Proximity: `"jakarta apache"~10` counts term movements, so order matters.
- Existence: `field:*` matches any value, including NaN and empty string.
- Ranges: `[52 TO 10000]` inclusive, `{Aida TO Carmen}` exclusive, mixed `{1 TO 10]`; `*` makes an end open. Non-numeric ranges sort lexicographically.
- Boost `^`, constant score `^=`.
- Operators `+`, `-`, `AND`/`&&`, `NOT`/`!`, `OR`; group with parentheses.

`sow` defaults to false, so whitespace-separated sequences are analyzed in one shot, which multi-word synonyms and shingles need.

Query analysis must be consistent with index analysis. Add `debug=true` to see the parsed query.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Standard Query Parser page: default "lucene" parser, `?` and `*` wildcards, fuzzy `~` with distance 0 to 2 defaulting to 2 and the fuzzy parser for `prefixLength`/`maxExpansions`, proximity as term movements, existence searches including NaN and empty values, range bracket forms and lexicographic ordering, `^=` constant score, OR as default operator, and `sow` default. Nothing removed.

Method: documentation only; no commands were run.
