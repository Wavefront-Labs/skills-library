---
id: computing-software.messaging-and-integration.apache-zookeeper.znode-types
name: znode-types
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, znode, persistent, ephemeral, sequential, container, ttl, data-model]
level: intro
status: docs-checked
description: "The ZooKeeper znode types: persistent, ephemeral, sequential, container and TTL nodes, their rules, versions introduced and limits."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperOver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Znode types

- Data at each znode is read and written atomically: a read gets all the bytes, a write replaces all of them. Each znode has an ACL and a stat structure.
- Persistent: stays until explicitly deleted.
- Ephemeral: exists as long as the creating session is active and is deleted when the session ends; ephemeral znodes cannot have children. `getEphemerals()` lists a session's ephemerals. Local sessions cannot create ephemeral nodes (they must be upgraded to global).
- Sequential (PERSISTENT_SEQUENTIAL, EPHEMERAL_SEQUENTIAL): ZooKeeper appends a counter to the name.
- Container (added in 3.5.3): special-purpose znodes for recipes such as leader and lock. When the last child is deleted the container becomes a candidate for deletion by the server later, so code creating children must handle `KeeperException.NoNodeException` and recreate the container.
- TTL (added in 3.5.3): PERSISTENT or PERSISTENT_SEQUENTIAL with a TTL in milliseconds; must be enabled by a system property (see ttl-nodes), otherwise `UnimplementedException`.
- The stat field `ephemeralOwner` is the owning session id for an ephemeral node, zero otherwise.

## Checked

Confirmed against the Programmer's Guide (Znodes, Ephemeral, Container, TTL, Zxid/stat and sessions sections). Removed the "per-parent" qualifier on the sequence counter, the unsourced zkCli Verify step, and the unconfirmed reference to size limits.

Method: docs-only read of cited pages, 2026-11-08
