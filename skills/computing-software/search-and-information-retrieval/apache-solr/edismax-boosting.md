---
id: computing-software.search-and-information-retrieval.apache-solr.edismax-boosting
name: edismax-boosting
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [edismax, pf-boost, phrase-boost, multiplicative-boost, user-fields]
level: practitioner
status: docs-checked
description: "Use the Solr eDisMax parser: mm defaults, boost multiplier, pf/pf2/pf3 phrase proximity boosts, sow, lowercaseOperators, stopword handling and uf field restrictions."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/edismax-query-parser.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# edismax-boosting

`defType=edismax` extends DisMax and keeps fielded queries, `+`/`-`, phrases and safe partial escaping on syntax errors.

Differences and parameters:
- `mm` default is 0% if the query has an explicit operator other than AND, or `q.op` is OR or unset; it is 100% if `q.op` is AND and no other explicit operators appear.
- `mm.autoRelax=true` relaxes the clause count when a stopword filter removes a clause from only some `qf` fields; use it for zero-hit problems from uneven stopwords.
- `boost`: functions multiplied into the score (equivalent to wrapping in the boost parser), unlike additive `bq`/`bf`.
- `pf`, `pf2`, `pf3`: boost documents where all terms, word pairs or word triplets are near each other; `ps`, `ps2`, `ps3` set slop.
- `sow` (default false), `lowercaseOperators` (default false).
- `uf` limits which fields users may query directly.
- Stopwords are not required in the mandatory part but still used for proximity boosting. A query of only stopwords requires all words, unless `alwaysStopwords` changes that.

Pure negative nested queries such as `+foo (-foo)` match all documents.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Extended DisMax Query Parser page: `mm` defaults, `mm.autoRelax`, `boost` as a multiplier, `pf`/`pf2`/`pf3` and `ps`/`ps2`/`ps3`, `sow` and `lowercaseOperators` defaults, `uf`, `alwaysStopwords`, stopword handling, smart partial escaping on syntax errors, and pure negative nested queries. Nothing removed.

Method: documentation only; no commands were run.
