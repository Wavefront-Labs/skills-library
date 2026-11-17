---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-write-modes
name: jaeger-es-write-modes
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, write-mode, async-sync, bulk-processing, elasticsearch-bulk]
level: advanced
status: docs-checked
description: "Choose async or sync write_mode for Elasticsearch and tune bulk_processing, knowing async hides write failures."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right durability behavior for _bulk writes.

```
elasticsearch:
  write_mode: async           # async (default) | sync
  poison_pill_handling: fail  # fail (default) | drop; only used in sync mode
  bulk_processing:
    max_bytes: 5000000        # per-request cap in both modes
    flush_interval: 200ms     # async mode only
    workers: 1                # async mode only
```
- async (default): spans go to a client-side buffer flushed by a background worker. The write returns before data is durable; a failed flush is logged and counted but the pipeline has already moved on. Highest throughput, lowest latency.
- sync: each batch from the pipeline becomes one blocking `_bulk` request that returns after Elasticsearch acknowledges, and returns an error if any span was not persisted. Cost: one `_bulk` round trip of latency per batch. Only `max_bytes` applies; a larger batch is split into several `_bulk` requests.

Async is the default because it costs the least, not because it is safer: the sender was told the spans were accepted, so it never retries or slows down. Sync returns failures to the pipeline; whether they reach the sender depends on the pipeline (see Delivery Guarantees skills).

## Checked

Method: docs-checked 2026-11-09 against the Jaeger 2.22 Elasticsearch storage page; the unconfirmed OpenSearch sentence was removed.
