---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.slow-log-configuration
name: slow-log-configuration
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, slow-log-configuration]
level: practitioner
status: docs-checked
description: "Enable per-index search and indexing slow logs in Elasticsearch with thresholds per level, user metadata and source truncation settings."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/slow-log
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search and indexing slow logs

**Goal:** a record of slow operations, set per index with `PUT <INDEX>/_settings`.
```
PUT my-index/_settings
{"index.search.slowlog.threshold.query.warn":"10s","index.search.slowlog.threshold.fetch.warn":"1s","index.indexing.slowlog.threshold.index.warn":"10s"}
```
- Thresholds: `index.search.slowlog.threshold.query.<level>`, `index.search.slowlog.threshold.fetch.<level>` and `index.indexing.slowlog.threshold.index.<level>`; `<level>` is `warn`, `info`, `debug` or `trace`. Values are a number plus unit such as `ms` or `s`. All thresholds default to `-1`, which disables slow logging.
- Search slow logs emit per shard and must be enabled separately for the query and fetch phases; indexing slow logs emit per document.
- Entries use fileset name `slowlog` and logger names `index.search.slowlog` or `index.indexing.slowlog`.
- `index.search.slowlog.include.user` and `index.indexing.slowlog.include.user` (boolean) add `user.*` and `auth.type` metadata about who made the request: decide whether that is acceptable in your log store.
- `index.indexing.slowlog.source` sets how many `_source` characters are logged: the first 1000 by default, `false` or `0` disables, `true` logs the whole source. `index.indexing.slowlog.reformat` defaults to `true` and puts the source on one line.
- The page recommends Elasticsearch query logging over slow logs for search (it measures end-to-end duration across Query DSL, ES|QL, EQL and SQL); slow logs remain the only option for indexing operations.

## Verify
- [ ] A deliberately slow query or large document shows up in the slow log at the expected level.

## Scope
Elasticsearch settings page only. The OpenSearch slow log setting names and file locations were not checked, and the log file name pattern is not stated on the page, so look up where your deployment writes logs.

## Checked

Checked 2026-11-08 against the Elasticsearch Slow log settings page. Confirmed: setting names, levels, the `-1` default, per-shard versus per-document emission, `include.user`, source length default and `reformat`. Removed: the log file name pattern and OpenSearch source root, which the page does not support.

Method: documentation only; no commands were run.
