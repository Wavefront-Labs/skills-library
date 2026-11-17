---
id: computing-software.data-engineering.apache-pinot.apache-pinot-deep-store-and-segment-recovery
name: apache-pinot-deep-store-and-segment-recovery
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, deep-store, segment-store, segment-completion-protocol, peer-download, disaster-recovery, pinotfs]
level: practitioner
status: docs-checked
description: "Role of the deep store: permanent segment copies, why ZooKeeper metadata is also required to restore, and how offline and realtime segments reach it."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/table/segment/deep-store.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep store and segment recovery

The deep store is the permanent store for segment files, used for backup and restore. New server nodes pull a copy of segment files from it, and if a server's local segment files are damaged or accidentally deleted, a new copy is pulled down on server restart.

It stores a compressed version of the segment files, typically without indexes, on a local file system or one of the supported file systems.

Restoring needs **both** the deep store and the Zookeeper metadata (table config, schema, segment metadata); the deep store alone is not sufficient.

How segments get there:
- Offline tables: the batch ingestion job writes the segment directly into the deep store, then notifies the controller, which notifies the appropriate server to pull it.
- Real-time tables, by default: the server builds the segment in memory, uploads it to the lead controller as part of the Segment Completion Protocol, and the controller writes it into the deep store.
- Because routing every segment through the controller can become a bottleneck under heavy load, you can use the peer download policy (see "Decoupling Controller from the Data Path" in the operate-pinot docs). Then the server writes the completed segment directly to the deep store.

For hands-on configuration see the S3 and OSS deep-storage tutorials in the Pinot docs.

## Checked

2026-11-08. Read the whole pinot-docs deep-store page. Confirmed the restore requirement, ingestion paths and the peer download policy. Corrected the peer-download description (the page says the server writes directly to the deep store, not that servers fetch from peers) and the claim that servers download on rebalance and reload; removed the throughput operational tip.

Method: documentation only; no commands were run.
