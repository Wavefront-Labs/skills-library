---
id: computing-software.search-and-information-retrieval.typesense.create-snapshot-backup
name: create-snapshot-backup
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [snapshot, backup, snapshot-path, typesense]
level: practitioner
status: docs-checked
description: "Back up a Typesense node with POST /operations/snapshot and snapshot_path, restore it as a data directory, and use a path-less internal snapshot for HA recovery."
sources: ["https://typesense.org/docs/30.2/api/cluster-operations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a snapshot

`POST /operations/snapshot?snapshot_path=<SNAPSHOT_DIR>` writes a point-in-time copy of the node's state and data into that directory on the server. Back up the resulting directory and later restore it by using it as the data directory. Send the `X-TYPESENSE-API-KEY` header.

## snapshot_path is optional

Without it Typesense performs an internal snapshot that compacts the Raft logs into the snapshot inside the process, without exporting data. This helps in certain scenarios when recovering a node in an HA cluster.

## Checked

Method: 2026-11-09 docs-only read of the cited Cluster Operations page in full. Confirmed endpoint, snapshot_path argument and the internal Raft-log snapshot behaviour. Removed the response body, client-library form and the snapshot-interval flag default, which the page does not show.
