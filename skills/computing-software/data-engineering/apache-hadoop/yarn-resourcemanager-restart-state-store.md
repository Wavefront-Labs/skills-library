---
id: computing-software.data-engineering.apache-hadoop.yarn-resourcemanager-restart-state-store
name: yarn-resourcemanager-restart-state-store
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, resourcemanager, recovery, state-store, zookeeper]
level: advanced
status: docs-checked
description: "YARN ResourceManager restart recovery: enabling it, choosing ZK, FileSystem or LevelDB state stores, their keys and defaults, and work-preserving recovery wait."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceManagerRestart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RM restart state store

Enable: `yarn.resourcemanager.recovery.enabled` = true. Pick `yarn.resourcemanager.store.class`: `ZKRMStateStore`, `FileSystemRMStateStore` (default) or `LeveldbRMStateStore`. Only ZooKeeper supports fencing for RM HA.

FileSystem store:
- `yarn.resourcemanager.fs.state-store.uri`, default `${hadoop.tmp.dir}/yarn/system/rmstore` (no scheme means `fs.defaultFS`)
- `yarn.resourcemanager.fs.state-store.retry-policy-spec`, default (2000, 500)

ZooKeeper store:
- `hadoop.zk.address`
- `yarn.resourcemanager.zk-state-store.parent-path`, default `/rmstore`
- `hadoop.zk.num-retries` 500, `hadoop.zk.retry-interval-ms` 2 seconds, `hadoop.zk.timeout-ms` 10 seconds
- `hadoop.zk.acl`, default `world:anyone:rwcda`

LevelDB store: `yarn.resourcemanager.leveldb-state-store.path`, default `${hadoop.tmp.dir}/yarn/system/rmstore`.

Work-preserving recovery: `yarn.resourcemanager.work-preserving-recovery.scheduling-wait-ms` delays new allocations after restart so NodeManagers can resync first.

Verify: with recovery enabled, restart the RM and confirm it reloads application state from the configured store.

## Checked
Confirmed 2026-11-08 against the Apache Hadoop ResourceManager Restart page: the enable key, the three store classes and the default, the FileSystem, ZooKeeper and LevelDB keys and defaults, ZooKeeper-only fencing, and the work-preserving recovery wait property.
Method: docs-only read of cited pages, 2026-11-08
