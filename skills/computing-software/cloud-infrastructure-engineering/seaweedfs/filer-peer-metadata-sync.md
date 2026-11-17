---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.filer-peer-metadata-sync
name: filer-peer-metadata-sync
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [peer-discovery, embedded-store, multiple-filers, metadata-sync]
level: advanced
status: docs-checked
description: "Scale out filers, even with embedded stores like LevelDB: masters tell filers about peers and each filer replays peer metadata changes locally."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Store-Replication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# filer peer metadata sync

Filers report themselves to the master, which keeps each filer informed of its peers (since version 2.77). Adding or removing a filer needs no config change, so rolling restarts are easy and Kubernetes can run filers as a ReplicaSet.

Each filer:
1. Aggregates metadata changes from peers (this is also what lets a FUSE mount, which streams changes from one filer, see writes made through other filers).
2. If its store is embedded (LevelDB, RocksDB, SQLite), replays those changes into the local store, so every filer holds a full copy of the metadata; this doubles as replication and high availability.

A new filer synchronizes automatically; a resumed filer continues from where it stopped.

Gotcha: multiple replicated embedded filers are only eventually consistent, so behind a load balancer it may not behave as expected; the page suggests hashing connections on the `uploadId` GET query or temporary sticky sessions. Shared-store plus embedded-store pairs do not replicate, and `weed filer.sync` does not cope with multiple `filer.store.id` values.

Verify: write via filer A, list via filer B after a moment.

## Checked
Checked 2026-11-09: peer discovery through the master since 2.77, no config change on add or remove, ReplicaSet in Kubernetes, FUSE mount aggregation, local replay for embedded stores, automatic and resumable sync, and eventual consistency match the Filer-Store-Replication page. Reworded the load-balancer advice to what the page says and added the unsupported-topology and filer.sync limits from it.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Filer-Store-Replication, read in full from a local clone of the wiki.
