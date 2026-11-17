---
id: computing-software.cloud-infrastructure-engineering.cortex.ingester-failure-wal-and-write-deamplification
name: ingester-failure-wal-and-write-deamplification
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ingester, wal, replication, data-loss, write-path]
level: advanced
status: docs-checked
description: "Explain how Cortex limits data loss when an ingester crashes using replication and the write-ahead log, and why ingesters batch writes."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ingesters keep recent samples in memory and flush them to long-term storage periodically, by default every 2 hours. Batching and compressing in memory is write de-amplification: flushing every sample straight to storage would put very high pressure on the store and be hard to scale. The docs call this the main source of Cortex's low total cost of ownership.

If an ingester crashes, in-memory series not yet flushed are lost unless mitigated. Two mechanisms:

1. Replication: typically 3 replicas of each series. A single ingester failure loses no samples because another replica holds them. Multiple simultaneous failures can lose data.
2. Write-ahead log (WAL): incoming samples are written to a persistent disk until flushed. After a restart the ingester replays the WAL and recovers its in-memory series. Unlike replication alone, this recovers even from multiple failures, provided the disks survive.

Replication is still recommended alongside the WAL so that a single ingester failure causes no temporary gaps on the read path.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page (raw markdown, read in full).
