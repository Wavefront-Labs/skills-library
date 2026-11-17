---
id: computing-software.messaging-and-integration.redpanda.write-caching-and-flush-settings
name: write-caching-and-flush-settings
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [write-caching, acks, fsync, flush-ms, durability, topic-properties]
level: advanced
status: docs-checked
description: "Trade durability for latency with write caching: write_caching_default, topic write.caching, flush.ms and flush.bytes, and the acks interaction."
sources:
  - https://docs.redpanda.com/streaming/current/develop/manage-topics/config-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Write caching is a relaxed mode of `acks=all`: a message is acknowledged once it is received and acknowledged on a majority of brokers, without waiting for the write to reach disk. It lowers latency while still requiring a majority.

**Scope.** It applies to user topics only. Transactional writes and consumer offset commits are always written and fsynced before acknowledgement.

**Defaults.** Enabled in development mode, disabled in production mode. Enable it only for workloads that tolerate some data loss if several brokers fail at once; leaving it off protects against loss of a whole data center or availability zone.

**Cluster level**
```bash
rpk cluster config set write_caching_default=true
```
Redpanda then fsyncs according to `raft_replica_max_pending_flush_bytes` and `raft_replica_max_flush_delay_ms`, whichever comes first.

**Topic level** overrides the cluster setting:
```bash
rpk topic alter-config my_topic --set write.caching=true
```
Redpanda then fsyncs according to `flush.ms` and `flush.bytes`, whichever comes first. If unset they inherit the cluster defaults: 100 ms and 256 KiB unless changed.

**Which requests the flush settings govern**
- `acks=0` or `acks=1`: always honor `flush.ms` and `flush.bytes`, with or without write caching.
- `acks=all`: honor them only when write caching is enabled. Otherwise each batch is fsynced on a majority of replicas before the write is acknowledged.

## Checked

2026-11-08. Read the whole Manage Topics page. Confirmed: write caching definition, user-topic scope with transactions and offset commits always fsynced, dev versus production defaults, data-loss and availability-zone caveat, cluster and topic commands, fsync property names, flush.ms and flush.bytes defaults of 100 ms and 256 KiB, acks interaction. Nothing removed.

Method: documentation only; no commands were run.
