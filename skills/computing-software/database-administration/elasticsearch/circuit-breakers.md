---
id: computing-software.database-administration.elasticsearch.circuit-breakers
name: circuit-breakers
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, circuit-breaker, parent-breaker, fielddata-breaker, request-breaker, circuit-breaking-exception, jvm-heap, indices-breaker-total-limit]
level: practitioner
status: verified
description: "Understand Elasticsearch circuit breakers (parent, fielddata, request, in-flight), diagnose circuit_breaking_exception 429s, and fix the cause instead of raising limits."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/circuit-breaker.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/circuit-breaker-errors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Circuit breakers

**Goal:** know why a request was refused with `circuit_breaking_exception` and stop it recurring without risking OutOfMemoryError.

## Breakers
| Breaker | Setting | Default | Guards |
|---|---|---|---|
| Parent | `indices.breaker.total.limit` | 95% heap (real memory) | Overall heap use |
| Fielddata | `indices.breaker.fielddata.limit` | 40% | Loading fielddata (text field aggs, legacy) |
| Request | `indices.breaker.request.limit` | 60% | Per-request structures (aggregation buckets) |
| In flight requests | `network.breaker.inflight_requests.limit` | 100% | Bytes of requests being received (bulk bodies) |

On 9.5.5 `GET _nodes/stats/breaker` lists `inflight_requests`, `request`, `fielddata`, `eql_sequence`, `model_inference` and `parent`; there is no `accounting` breaker and no `indices.breaker.accounting.limit` default (older versions had both).

The error (HTTP 429) names the breaker:
```
[parent] Data too large, data for [<http_request>] would be [123848638/118.1mb], which is larger than the limit of [123273216/117.5mb], real usage: [120182112/114.6mb], new bytes reserved: [3666526/3.4mb]
```

## Diagnose
```bash
GET _nodes/stats/breaker
GET _cat/nodes?v&h=name,heap.percent,heap.max
GET _cat/fielddata?v&s=size:desc
```
- `parent` trips repeatedly with high real usage: the heap really is full: heavy aggregations, too many shards per node, huge bulk requests, or GC not keeping up.
- `fielddata`: someone aggregates/sorts on a `text` field with `fielddata: true`. Use a `keyword` subfield; clear with `POST _cache/clear?fielddata=true`.
- `request`: a query building too many buckets; lower `size`/use composite, cap with `search.max_buckets`.
- `in_flight_requests`: bulk requests too large; send smaller batches.

## Fixes, in order
1. Fix the workload (smaller bulks, keyword fields, composite aggs, fewer shards).
2. Right-size the heap (follow the Elasticsearch JVM heap sizing guidance); more nodes rather than bigger heaps.
3. Only then adjust limits slightly; raising them trades 429s for OOM-crashed nodes.

## Gotchas
- Clients should treat 429 as retryable with backoff.
- Breakers estimate memory; an OOM can still occur with misbehaving scripts or plugins.

## Verify
`tripped` counts in `_nodes/stats/breaker` stop increasing and heap usage settles.
