---
id: computing-software.messaging-and-integration.apache-pulsar.architecture-brokers-bookies-metadata
name: architecture-brokers-bookies-metadata
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [architecture, brokers, bookkeeper, ledgers, managed-ledger, metadata-store, metadata-store-url]
level: practitioner
status: docs-checked
description: "Map a Pulsar cluster: stateless brokers, BookKeeper bookies and ledgers, managed ledgers, metadata store backends and the metadataStoreUrl forms."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-architecture-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which component owns which responsibility before sizing, scaling or debugging a cluster.

Pieces of a cluster:
- Brokers: stateless. Each runs an HTTP server (REST admin API and topic lookup) and a dispatcher, an asynchronous TCP server on a custom binary protocol for all data transfer. Messages are normally served from the managed ledger cache; only when the backlog outgrows the cache does the broker read entries from BookKeeper. Brokers also run geo-replication replicators.
- BookKeeper bookies: persistent storage of messages and of cursors (subscription positions). BookKeeper is a distributed write-ahead log. It scales horizontally; adding bookies increases capacity immediately. Bookies separate journal and general storage on different disks so reads do not hurt write latency.
- Metadata store: holds topic metadata, schemas, broker load data and ledger metadata. Backends: Oxia (recommended for new clusters), ZooKeeper (ships with the binary package), RocksDB (embedded, standalone only).
- Configuration store: an instance-wide metadata quorum for tenants, namespaces and other globally consistent entities; each cluster also has its own local metadata store.

Setting: `metadataStoreUrl`, for example `oxia://oxia-server:6648/broker`, `zk:my-zk-1:2181,my-zk-2:2181,my-zk-3:2181`, or `rocksdb:///path/to/data`. One metadata store cluster can serve both Pulsar and BookKeeper.

Ledgers: an append-only structure with one writer, replicated to several bookies. A ledger can be created, appended to and closed; once closed it opens read-only; whole ledgers are deleted when no longer needed. A managed ledger is the per-topic storage layer built on many BookKeeper ledgers, because a failed ledger is no longer writable and fully consumed ledgers can be deleted on rollover.

## Checked

2026-11-03. Confirmed against the pulsar-site page concepts-architecture-overview: broker, bookie, metadata store and configuration store roles, the three `metadataStoreUrl` forms, ledger and managed ledger semantics. Removed the invented Verify step.

Method: documentation only; no commands were run.
