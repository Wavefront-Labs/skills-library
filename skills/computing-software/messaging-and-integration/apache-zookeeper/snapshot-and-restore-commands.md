---
id: computing-software.messaging-and-integration.apache-zookeeper.snapshot-and-restore-commands
name: snapshot-and-restore-commands
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, snapshot, restore, adminserver, disaster-recovery, backup]
level: advanced
status: docs-checked
description: "Back up and recover ZooKeeper with the AdminServer snapshot and restore commands: curl examples, rate limit, auth requirements and the restore procedure."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperSnapshotAndRestore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot and restore via AdminServer

A cluster of N members tolerates up to (N-1)/2 permanent failures; beyond that it loses quorum and cannot accept updates. Snapshot and restore exist to recover from that.

- Both operate on the server you connect to, through the AdminServer APIs.
- Both are rate limited (once every 5 minutes by default).
- Both need authentication and authorization on the root path with ALL permission. Supported schemes: digest, x509 and IP.

Snapshot: take it periodically from a live server with the highest zxid and stream it to local or external storage (for example S3):
`curl -H 'Authorization: digest root:<PASSWORD>' 'http://hostname:adminPort/commands/snapshot?streaming=true' --output snapshotFileName`

Restore: takes one snapshot as an input stream. Use it for quorum loss or to build a brand-new cluster with seed data. All members restore the same snapshot:
`curl -H 'Content-Type:application/octet-stream' -H 'Authorization: digest root:<PASSWORD>' -POST http://hostname:adminPort/commands/restore --data-binary "@snapshotFileName"`

Recommended steps:
1. Block traffic on the client port or secure client port before restore starts.
2. If applicable, snapshot the latest database state with the snapshot command.
3. For each server, move the files in dataDir and dataLogDir elsewhere (so the restored database is not overwritten when the server restarts), then restore with the restore command.
4. Unblock client traffic after restore completes.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Snapshot and Restore Guide. Removed: the "Verify" step (`ls /` on every member) because the page gives no verification procedure.
