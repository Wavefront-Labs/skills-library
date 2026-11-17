---
id: computing-software.messaging-and-integration.apache-zookeeper.c-client-libraries
name: c-client-libraries
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, c-binding, zookeeper-mt, zookeeper-st, zookeeper-init, threaded]
level: advanced
status: docs-checked
description: "Choosing the ZooKeeper C client library: zookeeper_mt versus zookeeper_st, the -DTHREADED flag, and the zookeeper_init signature."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C binding

- Link `zookeeper_mt` for the threaded library with both sync and async APIs; it creates an IO thread and an event dispatch thread. Use it in all cases except platforms without a stable pthread library.
- Link `zookeeper_st` for async only, for integrating into an application's own event loop.
- Compile with `-DTHREADED` for the multithreaded build; do not define it for the single-threaded one.
- Start a handle with `zookeeper_init(host, fn, recv_timeout, clientid, context, flags)`.
- ACL constants are `ZOO_PERM_*` and the standard ACL lists are `ZOO_OPEN_ACL_UNSAFE`, `ZOO_READ_ACL_UNSAFE`, `ZOO_CREATOR_ALL_ACL`.
- The client server list may be a subset of the ensemble but must not name servers outside it.

Verify: the program links against the intended library and connects with the expected session timeout.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Programmer's Guide (C Binding, ACL constants and client server-list sections).
