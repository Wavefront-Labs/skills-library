---
id: computing-software.search-and-information-retrieval.qdrant.capacity-planning
name: capacity-planning
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [capacity-planning, sizing, memory-estimate, calculator, capacity]
level: practitioner
status: docs-checked
description: "Estimate Qdrant memory and disk needs from vector count, dimensions, datatype, quantization and payload."
sources:
  - "https://qdrant.tech/documentation/capacity-planning/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Size each collection separately, then sum. Start from the base unit: `base = number_of_points * replication_factor`.

Per-structure formulas from the docs (every structure is persisted to disk; the memory tier only decides what is also kept in RAM, where `pinned` is heap RAM, `cached` is memory-mapped and pre-warmed, and `cold` is memory-mapped on demand):

- Dense vectors: `base * dimensions * bytes_per_dim`. Bytes per dimension: float32 4 (default), float16 2, turbo16 2, uint8 1, turbo8 1, turbo4 0.5. One million points, 768 dimensions, replication 2, float32 is about 5.72 GB. Each named vector is sized separately.
- Quantized copy: `base * dimensions * quant_bytes`. With 4-bit TurboQuant (0.5 bytes), originals `cold` and the quantized copy `pinned`, RAM for the example drops from 5.72 GB to about 0.72 GB while disk stays close to the same. Check recall against unquantized results first.
- HNSW index: `base * m * 2 * 4 bytes * 1.2` (default `m` is 16), about 0.29 GB for the example. Default tier is `cached`; avoid `cold` because graph traversal does many small random reads.
- Sparse vectors: `base * nnz * bytes_per_dim`, and the index is that times 1.5. They need disk space and are not cached; sparse indexes default to `pinned`.
- Payload: disk `base * avg_payload_size * 1.5`, RAM three times that if cached. Payloads default to `cold`.
- Payload indexes: roughly twice the size of the indexed fields, default `pinned`. Index only fields you filter on. A per-element index adds about 4 bytes per point of RAM.
- ID tracker: `base * 52 bytes`, `pinned` by default.

Add about 20% headroom to the RAM and disk totals for the OS page cache, runtime overhead, optimizer temporary work, WAL, snapshots and temporary segments. Restoring a snapshot or using the Migration Tool needs twice the source collection's disk (and twice the RAM in use for the Migration Tool) on the target.

Topology:

- Nodes: `ceil(total_ram / (node_ram * 0.8))`. A single node typically tops out near 100 million vectors, a rough ceiling that depends on dimensions, datatype and quantization. For high availability use at least three nodes and replication of two or more.
- Shards: default to the node count at creation and cannot change without recreating the collection, except resharding in Qdrant Cloud. Use at least two per node to leave room to add nodes; 12 divides evenly across 1, 2, 3, 4, 6 and 12 nodes. A shard cannot be split across nodes.
- CPU: Qdrant uses up to 16 indexing threads by default; raise it on larger machines.

Disk over RAM: for on-disk vectors use local SSDs with at least 50k IOPS, and as a rule halving the vectors held in RAM roughly doubles search latency. The docs provide a sizing calculator at sizing.qdrant.tech; treat results as estimates and test with a representative sample.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant capacity planning page (landing_page repo, capacity-planning.md), read in full. Replaced the unconfirmed quantization ratios, "a few times raw size" disk rule and the raw-bytes-only formula with the page's formulas and tier defaults.
