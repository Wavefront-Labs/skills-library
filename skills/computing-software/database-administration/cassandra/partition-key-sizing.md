---
id: computing-software.database-administration.cassandra.partition-key-sizing
name: partition-key-sizing
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, partition-size, wide-partition, bucketing, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Keeping partitions bounded"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partition key choice and sizing

Goal: avoid hot and oversized partitions.
- Data-modelling guideline: under 100,000 values per partition and 100MB on disk.
- Bucket by time or hash: `PRIMARY KEY ((sensor_id, day), ts)`.
- `nodetool tablehistograms <ks> <table>` reports partition size and cell count percentiles.
- Unbounded per-entity append-only growth is the classic anti-pattern.
Verify: partition size percentiles stay under target.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: 100,000 values / 100MB guideline (data-modeling intro), tablehistograms output columns (troubleshooting page).
Removed: the tablestats max claim.
Method: documentation only; no commands were run.
