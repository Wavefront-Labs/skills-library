---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.thread-pool-rejections
name: thread-pool-rejections
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, thread-pool-rejections]
level: advanced
status: docs-checked
description: "Read _cat/thread_pool for search and write queues and rejections, and know how fixed pools size and reject work."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/thread-pool-settings
  - https://docs.opensearch.org/latest/api-reference/cat/cat-thread-pool/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread pool queues and rejections

**Goal:** tell saturation from misconfiguration.
- `GET _cat/thread_pool/search,write?v&h=node_name,name,active,queue,queue_size,rejected` (the `h` columns `active`, `queue`, `queue_size`, `rejected`, `pool_size`, `type`, `completed` are documented; `s` sorts, `format=json` for JSON). Needs the `monitor` cluster privilege. cat APIs are for humans; applications should use the nodes info API.
- `rejected` is the number of tasks rejected by the pool executor. A fixed pool queues work when all threads are busy; when a bounded queue is full it rejects further work, which typically fails the request.
- Elasticsearch defaults: `search` is fixed, size `int((processors * 3) / 2) + 1`, `queue_size` 1000 * size (since 9.0; fixed 1000 in 8.x and earlier). `write` is fixed, size = processors, `queue_size` `max(10000, processors * 750)` (10000 in 9.1 and earlier).
- Pool sizes derive from the detected processor count; set `node.processors` if it is detected wrongly or the node is CPU-limited. Check detected processors with the nodes info API `os` flag.
- Thread pool settings are static: edit `elasticsearch.yml` (for example `thread_pool.write.size`, `thread_pool.search.queue_size`). Scaling pools have an always-unbounded queue.
- Fix saturation by reducing or batching client load, adding nodes or optimising queries rather than only changing pool settings (judgement, not stated on the pages).
- OpenSearch has the same `_cat/thread_pool` endpoint (`v`, `h`, `s`, `local`, `format`); its page documents `cluster_manager_timeout`. Its default pool sizes were not checked.

## Verify
- [ ] The `rejected` counter stops growing under normal load.

## Checked
Checked 2026-11-08 against the Elasticsearch "Get thread pool statistics" API page and "Thread pool settings", and the OpenSearch "CAT Thread Pool API" page. Removed because not on the pages: the `es_rejected_execution_exception` name, HTTP 429 and exponential-backoff advice, and the claim that larger queues rarely help.
Method: documentation only; no commands were run.
