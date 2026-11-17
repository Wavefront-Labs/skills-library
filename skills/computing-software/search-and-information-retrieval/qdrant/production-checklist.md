---
id: computing-software.search-and-information-retrieval.qdrant.production-checklist
name: production-checklist
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [production, checklist, hardening, operations, prod-checklist]
level: practitioner
status: docs-checked
description: "Pre-production checklist for Qdrant: shards, payload partitioning, load balancing, access control and storage."
sources:
  - "https://qdrant.tech/documentation/production-checklist/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Before going live, the production checklist suggests checking:

Data layout

- Use a single collection with payload partitioning for tenants instead of many collections.
- Avoid too many shards: each collection has its own shards, so many collections multiply them. At a minimum, plan one shard or replica per node.
- Create payload indexes on filtered fields before ingesting data, since HNSW graphs are only optimized for payload filtering when built after the index exists.

Search quality

- Benchmark retrieval quality after applying quantization; some models cannot be quantized efficiently, and rescoring adds latency.
- Under heavy writes, query indexed data only (see the read-write contention skill).
- Evaluate hybrid search and reranking; delayed fan-outs query a second replica when the first is slow, for collections with replication factor above one.

Availability

- Put a load balancer in front of the nodes; Qdrant Cloud includes one, self-managed deployments must configure their own.

Security

- Set an API key, plus a read-only key for query-only consumers, and enable TLS.
- Bind to a private interface or loopback when self-hosting.
- Use fine-grained access control to give each client only the collections it needs.

Storage and hardware

- Choose a memory tier for vectors: `cached` is fastest but RAM becomes the bottleneck at scale; `cold` handles datasets larger than RAM.
- Estimate RAM before provisioning, with headroom for vector and payload index overhead.
- Use SSDs, not HDDs, for disk-backed storage.
- With vectors and the HNSW index in the `cold` tier, inline storage reduces I/O operations at the cost of more storage.

## Checked

2026-11-03. Confirmed on the Qdrant production checklist page: shard guidance, payload partitioning, payload indexes before ingestion, load balancer, API key and read-only key, TLS, private binding, fine-grained access, quantization benchmarking, memory tiers, SSDs, inline storage, delayed fan-outs. Removed items the page does not contain: three nodes, probes, strict-mode advice, ports 6334 and 6335, snapshots, metrics, quotas, open-file limit and the closing tip.

Method: documentation only; no commands were run.
