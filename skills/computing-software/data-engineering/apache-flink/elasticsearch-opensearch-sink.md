---
id: computing-software.data-engineering.apache-flink.elasticsearch-opensearch-sink
name: elasticsearch-opensearch-sink
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-elasticsearch, opensearch, elasticsearch-sink, bulk-indexing, idempotent-sink]
level: practitioner
status: docs-checked
description: "Write Flink streams to Elasticsearch or OpenSearch: bulk flush settings, document ids for idempotent upserts, at-least-once on checkpoint, failure handling and back pressure."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/elasticsearch/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/elasticsearch/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/opensearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elasticsearch / OpenSearch sink

Connectors: `flink-connector-elasticsearch7` (also an Elasticsearch 8 sink) and the OpenSearch connector, documented on the pages in `sources`.

## DataStream
```java
ElasticsearchSink<Order> sink = new Elasticsearch7SinkBuilder<Order>()
    .setHosts(new HttpHost("es", 9200, "https"))
    .setEmitter((o, ctx, indexer) -> indexer.add(
        Requests.indexRequest().index("orders-" + o.month()).id(o.id()).source(toMap(o))))
    .setBulkFlushMaxActions(1000)
    .setBulkFlushMaxSizeMb(5)
    .setBulkFlushInterval(2000)
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build();
stream.sinkTo(sink);
```
## SQL
```sql
CREATE TABLE orders_es (order_id STRING, status STRING, amount DOUBLE, PRIMARY KEY (order_id) NOT ENFORCED)
WITH ('connector'='elasticsearch-7', 'hosts'='https://es:9200', 'index'='orders',
      'sink.bulk-flush.max-actions'='1000', 'sink.bulk-flush.interval'='2s');
```
With a PRIMARY KEY the sink upserts (and deletes on retractions) using the key as `_id`; without it, appends with auto ids.

## Delivery semantics
- `AT_LEAST_ONCE` is the default delivery guarantee. Checkpointing is not enabled by default; without it the sink buffers requests until the BulkProcessor flushes (by default after 1000 actions). With checkpoints, pending requests are flushed before the checkpoint completes.
- Make writes **idempotent** with a deterministic `_id` (business key): the docs note that `UpdateRequest`s with deterministic ids and upsert give exactly-once results under `AT_LEAST_ONCE`. Auto-generated ids + at-least-once = duplicates.

## Failure handling
- With a backoff strategy the sink re-adds requests that failed from resource constraints (such as queue saturation); for other failures such as malformed documents the sink fails. With no strategy (or `FlushBackoffType.NONE`) it fails on any error. Validate documents before the sink.
- Re-added requests lengthen checkpoints, since the checkpoint waits for them to flush. The backoff strategy is not supported by the Elasticsearch 8 sink.

## Verify
- [ ] Kill the job and restore: document count equals distinct ids from the source (no duplicates).
- [ ] Elasticsearch write rejections are not rising.

## Checked
2026-10-31. Confirmed against the Flink stable Elasticsearch DataStream, Elasticsearch table and OpenSearch DataStream pages: builder methods, `FlushBackoffType.EXPONENTIAL`, `sink.bulk-flush.*` options, the `elasticsearch-7` connector value, default AT_LEAST_ONCE, deterministic-id upsert, failure behaviour. Removed: delivery-guarantee and credential setter calls, external versioning, refresh-interval tip, metric name, the opensearch artifact name (not found on these pages).
Method: documentation only; no commands were run.
