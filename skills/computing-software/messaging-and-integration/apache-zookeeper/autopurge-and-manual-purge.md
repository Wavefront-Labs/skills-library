---
id: computing-software.messaging-and-integration.apache-zookeeper.autopurge-and-manual-purge
name: autopurge-and-manual-purge
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, autopurge, purgetxnlog, zkcleanup, maintenance, retention]
level: practitioner
status: docs-checked
description: "Clean old ZooKeeper snapshots and logs: autopurge.snapRetainCount and purgeInterval, PurgeTxnLog and zkCleanup.sh usage and retention rules."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Purging snapshots and logs

With the default configuration a server does not remove old snapshots and log files; that is the operator's job.

Automatic (since 3.4.0), in `zoo.cfg`:
- `autopurge.snapRetainCount`: retains this many most recent snapshots and the matching transaction logs in dataDir and dataLogDir, deleting the rest. Defaults to 3; minimum 3.
- `autopurge.purgeInterval`: hours between purge runs. A positive integer (1 and above) enables it; default 0.

Manual:
- `org.apache.zookeeper.server.PurgeTxnLog <dataDir> <snapDir> -n <count>` (run with `java -cp` including zookeeper.jar, the slf4j/logback jars from `lib/` and `conf`) keeps the last count snapshots and their logs. The guide says count should typically be greater than 3 (not required; it leaves 3 backups if a recent log is corrupted) and suggests a daily cron job on each server.
- `zkCleanup.sh` usage: `dataLogDir [snapDir] -n count`; count is the number of old snaps/logs to keep and must be 3 or more. Example: `./zkCleanup.sh -n 5` keeps the latest 5 logs and snapshots.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Administrator's Guide (Ongoing Data Directory Cleanup, autopurge options) and the Tools page (zkCleanup.sh). Removed: the "Verify" claim that the number of `snapshot.*` files equals the retain count (not stated on the pages).
