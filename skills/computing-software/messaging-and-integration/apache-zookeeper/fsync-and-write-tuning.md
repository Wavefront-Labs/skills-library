---
id: computing-software.messaging-and-integration.apache-zookeeper.fsync-and-write-tuning
name: fsync-and-write-tuning
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, fsync, forcesync, flushdelay, maxbatchsize, response-cache, write-tuning]
level: advanced
status: docs-checked
description: "Write path knobs: fsync.warningthresholdms, forceSync, flushDelay, maxBatchSize and response cache sizes with defaults, and the risk of disabling sync."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write-path tuning

- `fsync.warningthresholdms` (`zookeeper.fsync.warningthresholdms`): default 1000; logs a warning when an fsync exceeds it.
- `forceSync` (`zookeeper.forceSync`): requires log updates to reach media before completing; set to no to disable. The guide lists it as an unsafe option and gives no default.
- `flushDelay` (`zookeeper.flushDelay`): default 0 ms commit log flush delay.
- `maxWriteQueuePollTime`: default flushDelay / 3, relevant only when flushDelay is enabled.
- `maxBatchSize`: default 1000 transactions before a flush.
- `maxResponseCacheSize` and `maxGetChildrenResponseCacheSize`: default 400; 0 or negative disables.
- `syncEnabled` (`zookeeper.observer.syncEnabled`): default true; observers persist transactions and snapshots.
- `skipACL` skips ACL checks (full access) and is unsafe.

Verify: no fsync warnings appear in the log under load (the threshold is `fsync.warningthresholdms`).

## Checked

Read the relevant entries of the ZooKeeper Administrator's Guide. Confirmed fsync.warningthresholdms (default 1000 ms), forceSync, flushDelay, maxWriteQueuePollTime, maxBatchSize, the response cache sizes (default 400, 0 or negative disables), syncEnabled, and skipACL. Removed the example Prometheus alert rule on fsynctime_sum, which the guide does not give.

Method: docs-only read of cited pages, 2026-11-08
