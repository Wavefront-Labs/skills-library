---
id: computing-software.messaging-and-integration.apache-zookeeper.ttl-nodes
name: ttl-nodes
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, ttl-nodes, extendedtypesenabled, unimplementedexception, create-t]
level: practitioner
status: docs-checked
description: "Using ZooKeeper TTL znodes: enabling with extendedTypesEnabled, create -t in milliseconds, expiry conditions and the myid range side effect."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL nodes

- Added in 3.5.3 (Programmer's Guide). Disabled by default. Creating one without the system property throws `KeeperException.UnimplementedException`.
- Enable with the Java system property `zookeeper.extendedTypesEnabled=true` (system property only, not a zoo.cfg key; new in 3.5.4 and 3.6.0).
- Enabling extended types means server ids must be less than 255; the myid guide gives 1-254 instead of 1-255.
- Only PERSISTENT and PERSISTENT_SEQUENTIAL znodes can have a TTL, in milliseconds.
- A znode not modified within the TTL and with no children becomes a candidate for deletion by the server at some point in the future, so removal is not instantaneous.
- zkCli: `create [-s] [-e] [-c] [-t ttl] path [data] [acl]`, for example `create -t 3000 /ttl_node mydata`.
- Candidate container and TTL nodes are checked every `znode.container.checkIntervalMs` (system property only, default 60000) and at most `znode.container.maxPerMinute` (default 10000) are deleted per minute.

## Checked

Confirmed against Programmer's Guide (TTL Nodes), Administrator's Guide (myid, extendedTypesEnabled, znode.container.* properties) and the CLI guide (create syntax and example). Removed the unsourced "Verify" step and the claim that the key is a zoo.cfg setting.

Method: docs-only read of cited pages, 2026-11-08
