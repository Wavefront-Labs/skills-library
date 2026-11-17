---
id: computing-software.messaging-and-integration.apache-zookeeper.tutorial-java-barrier-and-queue
name: tutorial-java-barrier-and-queue
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, tutorial, java, syncprimitive, barrier, producer-consumer]
level: intro
status: docs-checked
description: "The ZooKeeper Java tutorial: SyncPrimitive base class with a 3000 ms session, Barrier enter/leave, queue produce/consume and the qTest/bTest demo commands."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperTutorial.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java tutorial structure

- `SyncPrimitive` implements `Watcher`: a static ZooKeeper handle created once with a 3000 ms session timeout, a static mutex for wait/notify, and `process(WatchedEvent)` that notifies waiting threads.
- Barrier(address, root, size): creates a persistent root (e.g. `/b1`); `enter()` creates an ephemeral child named after the host then waits via `getChildren(root, true)` until the child count equals the group size; `leave()` deletes its child and waits for the others.
- Queue(address, root): `produce(int)` creates a PERSISTENT_SEQUENTIAL "element" with a 4-byte integer; `consume()` lists children with a watch, picks the smallest numeric suffix, reads then deletes it.
- Demo: `qTest <server> <count> p|c` and `bTest <server> <participants>`, run via `zkEnv.sh`.

Verify: start a producer for 100 elements and then a consumer for 100; the consumer prints an `Item:` line per element consumed.

## Checked

Method: docs-checked 2026-11-09 against zookeeperTutorial.html (full page read, including the complete source listing)
