---
id: computing-software.search-and-information-retrieval.apache-solr.join-query-parser
name: join-query-parser
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [join-parser, join-query-parser, cross-collection-join, fromindex, dvwithscore, query-time-join]
level: advanced
status: docs-checked
description: "Use the Solr join query parser with from, to, fromIndex and method (index, dvWithScore, topLevelDV, crossCollection); know its filtering-only limits and cross-collection rules."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/join-query-parser.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# join-query-parser

`q={!join from=manu_id_s to=id}title:ipod` runs the sub-query, collects the values of the `from` field in matching documents, and returns documents whose `to` field contains those values, like a SQL `IN` sub-select.

Cross-core: add `fromIndex=movie_directors` with `from=id to=director_id`, as in `fq={!join from=id fromIndex=movie_directors to=director_id}has_oscar:true`. You cannot return fields from the `fromIndex` collection; it only filters the `to` side. In SolrCloud the `fromIndex` collection must have a single shard with a replica on every node hosting the `to` collection, unless the `crossCollection` method is used. A `router.field` equal to the join key can co-locate data.

`method`:
- `index` (default unless `score` is given): scales with the cardinality and postings of the `from` field; good for low-cardinality `from` fields or when many `to` documents match.
- `dvWithScore` (implied by `score`): required for scores; supports docValues numeric `from` fields.
- `topLevelDV`: better as matched values grow, if post-commit slowness is tolerable.
- `crossCollection`: join across collections, for example with `fromIndex="otherCollection"`.


## Checked

2026-11-04. Confirmed against the Solr Reference Guide Join Query Parser page: the `from`/`to` semantics, `fromIndex` examples and the filtering-only limit, the single-shard SolrCloud requirement, `router.field` guidance, `method` options and defaults, `score` implying `dvWithScore`, and the `crossCollection` example. Removed the closing advice to prefer block join, which the page does not state.

Method: documentation only; no commands were run.
