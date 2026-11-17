---
id: computing-software.messaging-and-integration.apache-zookeeper.snapshot-inspection-tools
name: snapshot-inspection-tools
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, snapshotformatter, snapshot-comparer, recursive-summary, zksnapshottoolkit, troubleshooting]
level: advanced
status: docs-checked
description: "Inspect ZooKeeper snapshots offline: zkSnapShotToolkit -d and -json, the recursive summary toolkit, and zkSnapshotComparer options and interactive mode."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot tools

- `zkSnapShotToolkit.sh`: usage `SnapshotFormatter [-d|-json] snapshot_file`. With no flag it prints each znode's metadata (cZxid, ctime, mZxid, mtime, pZxid, cversion, dataVersion, aclVersion, ephemeralOwner, dataLength); `-d` dumps the data for each znode (the page's sample shows it base64-encoded); `-json` dumps znode info as JSON.
- `zkSnapshotRecursiveSummaryToolkit.sh <snapshot_file> <starting_node> <max_depth>`: child count and data size for the starting node. `max_depth` 0 means no depth limit; 1 shows the starting node and its children; it affects only what is displayed, not the calculation.
- `zkSnapshotComparer.sh`: loads two snapshots and reports znode paths added, updated or deleted. Only permanent nodes are reported (sessions and ephemeral nodes ignored). Reads uncompressed, snappy and gz snapshots, and different formats can be compared directly.
  - Required: `-b/--bytes` node data delta threshold in bytes, `-n/--nodes` descendant node delta threshold, `-l/--left` and `-r/--right` snapshot files.
  - Optional: `-i/--interactive`, `-d/--debug`.
  - Interactive mode: Enter prints the current depth layer, a number jumps to that depth (out-of-range is rejected with the valid range), an absolute path starting with `/` prints that node's immediate subtree, `^c` exits at any time; it exits itself when all layers are compared. Only results passing the bytes and nodes thresholds are shown.
  - Example from the page: `./bin/zkSnapshotComparer.sh -l /zookeeper-data/backup/snapshot.d.snappy -r /zookeeper-data/backup/snapshot.44 -b 2 -n 1`.

Snapshots live in the data directory configured in `conf/zoo.cfg`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the whole Tools page. Removed: the "Verify" line (the formatter output matching expectations is not a documented check).
