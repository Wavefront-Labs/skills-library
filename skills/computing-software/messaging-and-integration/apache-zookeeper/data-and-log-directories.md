---
id: computing-software.messaging-and-integration.apache-zookeeper.data-and-log-directories
name: data-and-log-directories
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, datadir, datalogdir, transaction-log, snapshot-files, disk-layout]
level: practitioner
status: docs-checked
description: "Where ZooKeeper keeps data: dataDir versus dataLogDir, why the log needs a dedicated device, file naming and the fact that the server never deletes files."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data and log directories

- `dataDir` holds snapshots (`snapshot.*`), `myid`, and the `initialize` marker; unless `dataLogDir` is set it also holds the transaction log.
- `dataLogDir` sends the transaction log to a separate directory.
- Put the log on a dedicated device. A dedicated partition on a shared device is not enough: ZooKeeper writes the log sequentially and syncs before acknowledging, so other processes' contention can cause delays of several seconds.
- Snapshot files are fuzzy; the suffix is the zxid of the last committed transaction when the snapshot began. Log file names end with the first zxid they contain.
- A new log starts at a threshold derived from `snapCount` and `snapSizeLimitInKb`.
- ZooKeeper never deletes snapshots or logs by itself; enable autopurge or purge externally.

Verify: `ls` of dataLogDir shows the transaction log files and dataDir shows `snapshot.*` files plus `myid`.

## Checked

Method: docs-checked 2026-11-09 against zookeeperAdmin.html (Single Machine Requirements and Data File Management sections) and zookeeperStarted.html (full page read)
