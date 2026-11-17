---
id: computing-software.database-administration.elasticsearch.esql-piped-queries
name: esql-piped-queries
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, esql, es-ql, elasticsearch-query-dsl, piped-query-language]
level: practitioner
status: verified
description: "Query Elasticsearch with ES|QL piped syntax (FROM, WHERE, EVAL, STATS, ENRICH, LOOKUP JOIN) via _query API, and know its limits versus Query DSL."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-rest.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-limitations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ES|QL piped queries

**Goal:** ad-hoc analysis and dashboards with a readable pipeline language instead of nested JSON aggregations.

## Run
```bash
curl -s -u elastic --cacert ca.crt -H 'Content-Type: application/json' \
  "https://es:9200/_query?format=txt" -d '{
  "query": "FROM logs-* | WHERE @timestamp > NOW() - 1 hour AND http.response.status_code >= 500 | STATS errors = COUNT(*) BY service.name | SORT errors DESC | LIMIT 10"
}'
```
`format`: `json` (default), `txt`, `csv`, `tsv`. Kibana Discover has an ES|QL mode.

## Core commands
```esql
FROM orders-*
| WHERE status == "paid" AND total > 100
| EVAL total_eur = total * 0.92, day = DATE_TRUNC(1 day, @timestamp)
| STATS revenue = SUM(total_eur), n = COUNT(*) BY day, country
| SORT day DESC
| KEEP day, country, revenue, n
| LIMIT 1000
```
Also: `DISSECT`/`GROK` (parse strings at query time), `ENRICH` (needs an executed enrich policy; unmatched rows get null), `LOOKUP JOIN` (joins an index created with `"index.mode": "lookup"`), `MV_EXPAND`, `RENAME`, `DROP`, `ROW` for testing expressions.

## Parameters (avoid string building)
```json
{ "query": "FROM logs-* | WHERE service.name == ?svc | LIMIT 10", "params": [ { "svc": "checkout" } ] }
```

## Limits to know
- Without `LIMIT` a query returns at most 1,000 rows (`esql.query.result_truncation_default_size`); the largest `LIMIT` honoured is 10,000 (`esql.query.result_truncation_max_size`); both are cluster settings.
- Check the `columns` types in each response; not every field type is supported by every function.
- Async variant `_query/async` for long queries.
- Cross-cluster `FROM remote:logs-*` needs a configured remote cluster and an Enterprise (or trial) licence: on the Basic licence the request failed with "A valid Enterprise license is required to run ES|QL cross-cluster searches".
- Not a replacement for relevance search: use Query DSL for scoring, highlighting, `search_after` paging.

## Verify
Compare an ES|QL `STATS` result with the equivalent aggregation for one known window; check the response `columns` types are as expected.
