---
id: computing-software.data-engineering.trino.trino-exchange-properties
name: trino-exchange-properties
category: computing-software
field: data-engineering
product: trino
tags: [exchange, exchange-client-threads, exchange-max-buffer-size, sink-max-buffer-size, compression-codec]
level: advanced
status: docs-checked
description: "Tune Trino inter-node data transfer with the exchange and sink buffer properties, concurrency multiplier, compression and integrity checks."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/properties-exchange.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino exchange properties

Exchanges move data between Trino nodes between query stages. Adjust these properties to fix inter-node communication problems or improve network use.

Exchange client properties:
- `exchange.client-threads` (default `25`, min 1): threads fetching data from other nodes. More can help big or highly concurrent clusters; too many costs context switches and memory.
- `exchange.concurrent-request-multiplier` (default `3`): scales the heuristic for concurrent requests. With `exchange.max-buffer-size` of 32MB, 20MB used and 2MB average request, clients = multiplier * ((32-20)/2) = multiplier * 6.
- `exchange.max-buffer-size` (default `32MB`): client buffer for fetched data; larger improves throughput on bigger clusters but takes memory.
- `exchange.max-response-size` (default `16MB`, min 1MB): raise it for high-latency networks; lower it on large clusters to reduce skew.
- `exchange.compression-codec` (`NONE`, `LZ4`, `ZSTD`; default `NONE`): applies to node-to-node exchange and to exchange storage in fault-tolerant execution.
- `exchange.data-integrity-verification` (`NONE`, `ABORT`, `RETRY`; default `ABORT`): abort the query, disable checks, or repeat the exchange on corruption.

Sink (output) properties:
- `sink.max-buffer-size` (default `32MB`): task output waiting for upstream pulls; shared across partitioned consumers when hash partitioned. Raise for high latency or many nodes.
- `sink.max-broadcast-buffer-size` (default `200MB`): holds build-side data for replicated joins. Too small prevents probe-side tasks scaling when nodes are added.

The HTTP client used for exchanges is configured separately.

## Checked

2026-11-04. Read against the Trino docs page `admin/properties-exchange.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
