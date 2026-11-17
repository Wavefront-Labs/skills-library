---
id: computing-software.search-and-information-retrieval.apache-solr.rerank-query
name: rerank-query
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [rerank, rq-parameter, rerank-qparser, rank-query, reranking]
level: practitioner
status: docs-checked
description: "Re-rank the top Solr results with rq={!rerank}: reRankQuery, reRankDocs, reRankWeight and reRankScale, so expensive scoring runs only on the top N."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/query-re-ranking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rerank-query

Run a cheap main query, then re-score only the top N documents with a costlier query. Specify it with the `rq` parameter, which must parse to a RankQuery. Parsers shipped: `rerank` (ReRankQParserPlugin), `xport` and `ltr`.

`rerank` local params:
- `reRankQuery` (required): the second-phase query.
- `reRankDocs` (default 200): top documents to re-rank; treated as a minimum and may be raised to cover `start+rows`.
- `reRankWeight` (default 2.0): multiplier on the rerank score before it is combined with the original score.
- `reRankScale`: rescale rerank scores into a `min-max` range, for example 0-1.
- `reRankMainScale`: similar scaling for the main score.

Trade-off: a document scoring very low in the main query may never reach the re-ranking phase even if it would score highly under the second query.

Pass the second query by reference, for example `rq={!rerank reRankQuery=$rqq reRankDocs=100}` with a separate `rqq` parameter.

## Checked

2026-11-04. Confirmed against the Query Re-Ranking page and the Dense Vector Search page (which uses the `rq={!rerank reRankQuery=$rqq reRankDocs=100 ...}` form): `rq`, rerank parameters and defaults. Changed the example to `reRankDocs=100` as shown there; removed generic advice.

Method: documentation only; no commands were run.
