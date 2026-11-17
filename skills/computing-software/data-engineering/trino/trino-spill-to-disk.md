---
id: computing-software.data-engineering.trino.trino-spill-to-disk
name: trino-spill-to-disk
category: computing-software
field: data-engineering
product: trino
tags: [spill, spill-to-disk, revocable-memory, spiller-spill-path, spill-encryption]
level: advanced
status: docs-checked
description: "How Trino spills joins, aggregations, ORDER BY and window functions to disk, the spill path, compression and encryption trade-offs, and why it is legacy."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/spill.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino spill to disk

Spill-to-disk lets memory-intensive operations offload intermediate results so queries can exceed per-query or per-node memory limits. The docs call it legacy functionality and advise considering fault-tolerant execution with the `task` retry policy and an exchange manager instead.

Mechanism: normally Trino kills a query that exceeds `query_max_memory` or `query_max_memory_per_node`. With revocable memory, a query can request memory that does not count toward limits but can be revoked at any time; on revocation the query spills intermediate data and processes it later. A spilling query can run orders of magnitude slower than an in-memory one, and spill does not guarantee success: chunks may still be too large, giving out-of-memory errors when reloaded.

Disk guidance:
- Spill is IO heavy; give `spiller-spill-path` multiple paths on separate local devices. Trino treats them as independent disks (JBOD), so RAID is unnecessary.
- Never use the system drive or the drive where the JVM writes logs; it can destabilise the cluster. Monitor disk saturation.
- `spill-compression-codec` cuts IO for extra CPU.
- `spill-encryption-enabled` uses a random per-file key, costs CPU and throughput; consider lowering `memory-revoking-threshold` with it.

Supported operations:
- Joins: the build table is partitioned by `task.concurrency`; a subset of partitions (plus matching probe rows) spills and is read back one by one, so peak memory approaches 1 / task.concurrency of the build table, assuming no skew.
- Aggregations, ORDER BY: partial results go to disk and are merged back.
- Window functions: spill does not work in all cases, for example one very large window.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
