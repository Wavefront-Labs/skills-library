---
id: computing-software.messaging-and-integration.apache-zookeeper.stat-structure
name: stat-structure
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, stat, czxid, mzxid, version, cversion, aversion, ephemeralowner]
level: practitioner
status: docs-checked
description: "Fields of the ZooKeeper Stat structure: zxids, times, data/children/ACL version numbers, ephemeralOwner, dataLength and numChildren, and optimistic updates."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stat structure

Fields (Programmer's Guide): czxid (zxid of the change that created the znode), mzxid (last modified), pzxid (last change to its children), ctime and mtime (milliseconds from epoch of creation and last modification), version (changes to data), cversion (changes to children), aversion (changes to the ACL), ephemeralOwner (session id of the owner if ephemeral, otherwise zero), dataLength, numChildren.

- Every change gets a zxid, which exposes the total ordering of all changes; if zxid1 is smaller than zxid2, zxid1 happened before zxid2.
- ZooKeeper uses real time only for the timestamps in the stat structure on creation and modification.
- zkCli (Getting Started) prints the stat as cZxid, ctime, mZxid, mtime, pZxid, cversion, dataVersion, aclVersion, ephemeralOwner, dataLength, numChildren. In the guide's example a `set` raises mZxid from 5 to 6 and dataVersion from 0 to 1.
- Conditional operations: `set [-s] [-v version] path data` and `delete [-v version] path`. The CLI guide describes `set -v` as setting data with CAS, with the version taken from dataVersion via `stat`.

## Checked

Confirmed against the Programmer's Guide (Stat Structure, Zxid, Version numbers, Real time) and the Getting Started and CLI pages. Removed the unsourced Verify step and the "optimistic update" detail beyond the documented CAS note.

Method: docs-only read of cited pages, 2026-11-08
