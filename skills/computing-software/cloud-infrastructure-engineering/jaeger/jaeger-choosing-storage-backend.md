---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-choosing-storage-backend
name: jaeger-choosing-storage-backend
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, opensearch-vs-cassandra, storage-recommendation, write-amplification, data-ttl]
level: practitioner
status: docs-checked
description: "Weigh OpenSearch against Cassandra for Jaeger storage using the documented search, write-amplification and TTL tradeoffs."
sources:
  - https://www.jaegertracing.io/docs/2.22/faq/
  - https://www.jaegertracing.io/docs/2.22/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose a primary storage.

Supported: Cassandra, Elasticsearch and OpenSearch are the primary distributed backends; ClickHouse is an experimental backend behind a feature gate. For large-scale production the Jaeger team recommends OpenSearch over Cassandra, and the FAQ recommends Elasticsearch or OpenSearch over Cassandra.

FAQ reasoning:
- Search: Cassandra is a key-value store, efficient for trace-ID lookup, but Jaeger implements search on the client side on top of it, which is limited and may produce inconsistent results (issue 166). OpenSearch does not have this issue, can be queried directly (for example from Kibana) and offers analytics and aggregations.
- Write throughput: single writes were observed to be much faster in Cassandra, but writing a span there causes large write amplification: extra writes for service name and operation name indexing plus index writes for every tag. A span in OpenSearch is a single write with indexing inside the node. Overall throughput is comparable.
- Maintenance: Cassandra has native data TTL; OpenSearch expiration is managed through index rotation, which needs extra setup (Elasticsearch rollover).

## Checked

2026-11-08: read the whole FAQ and the whole Storage Backends index page (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed the supported backends, the recommendation and all three tradeoffs. Removed unsupported claims: Badger and memory being single-node, the backend version support list, and ScyllaDB as a drop-in.

Method: documentation only; no commands were run.
