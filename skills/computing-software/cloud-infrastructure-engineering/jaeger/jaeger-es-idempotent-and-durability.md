---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-es-idempotent-and-durability
name: jaeger-es-idempotent-and-durability
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, idempotent-writes, translog-durability, refresh-interval, elasticsearch-durability]
level: advanced
status: docs-checked
description: "Understand Elasticsearch idempotent span ids, translog durability and why acknowledged spans may not be searchable yet."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/elasticsearch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reason correctly about retries and visibility.

Idempotent writes: every span document has a deterministic `_id` derived from its content, in both write modes. Rewriting the same span overwrites the document, so a batch retried after a lost acknowledgement leaves exactly one copy. Elasticsearch enforces `_id` uniqueness only within one index, so a retry landing after an alias or data stream rolled over writes a second copy into the new index. A span whose document cannot be JSON-encoded (for example an attribute holding NaN) is logged and skipped. Client-supplied ids disable the auto-id fast path, a small per-document indexing cost.

Durability versus searchability: a successful `_bulk` response means documents are durable, not yet searchable. That holds under the default `index.translog.durability: request`; an index set to `async` acknowledges before the translog is synced, so a backend crash can lose acknowledged documents.

Search visibility follows the index refresh interval, one second by default. Jaeger does not ask Elasticsearch to refresh on write, because forced refreshes reduce indexing throughput without improving durability. In sync mode a span is acknowledged up to one refresh interval before it appears in search results.

## Checked

The idempotent id behaviour, rollover caveat, NaN skip, translog durability and refresh interval statements were confirmed in the Idempotent writes and Durability versus searchability sections of the Elasticsearch storage page. The page header marks version 2.22 as outdated in favour of 2.23.

Method: docs-checked 2026-11-09 against the Jaeger 2.22 Elasticsearch storage page (Write Modes through Poison pills sections read from a downloaded copy, plus keyword search of the rest).
