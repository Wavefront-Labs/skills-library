---
id: computing-software.messaging-and-integration.apache-zookeeper.snapshot-triggers-and-compression
name: snapshot-triggers-and-compression
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, snapcount, snapsizelimitinkb, preallocsize, snapshot-compression, digest]
level: advanced
status: docs-checked
description: "When ZooKeeper snapshots: snapCount randomisation, snapSizeLimitInKb, preAllocSize, txnLogSizeLimitInKb, snapshot.compression.method and tree digest settings."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot triggers and compression

- `snapCount` (`zookeeper.snapCount`), default 100000: a snapshot is taken after a random number of transactions in [snapCount/2+1, snapCount], so quorum members do not snapshot together.
- `snapSizeLimitInKb` (`zookeeper.snapSizeLimitInKb`), default 4194304 (4 GB): size-based trigger; non-positive disables.
- `preAllocSize` (`zookeeper.preAllocSize`), default 64M: log preallocation block.
- `txnLogSizeLimitInKb`: off by default; rolls the log at a size limit.
- `snapshot.compression.method`: default empty (none); `gz` or `snappy`.
- `snapshot.trust.empty`: default false; only for upgrades from pre-3.5.3.
- `digest.enabled`: default true; tree digest for inconsistency detection, stored in transactions and snapshots.
- `serializeLastProcessedZxid.enabled`: default true; needed for the snapshot/restore admin commands.
- `commitLogCount`: default 500 committed requests kept in memory for fast follower sync.

Verify: a new snapshot is written once the transaction log reaches the randomised threshold described under snapCount.

## Checked

Read the relevant entries of the ZooKeeper Administrator's Guide. Confirmed snapCount and its randomised range, snapSizeLimitInKb, preAllocSize, txnLogSizeLimitInKb, snapshot.compression.method values, snapshot.trust.empty, digest.enabled (default enabled, digests persisted with transactions and snapshots), serializeLastProcessedZxid.enabled, and commitLogCount. Reworded the verify step to avoid an unsourced file-name pattern.

Method: docs-only read of cited pages, 2026-11-08
