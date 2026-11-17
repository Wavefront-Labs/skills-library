---
id: computing-software.messaging-and-integration.apache-zookeeper.recipe-locks
name: recipe-locks
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, recipes, distributed-lock, locknode, ephemeral-sequential, herd-effect]
level: practitioner
status: docs-checked
description: "ZooKeeper exclusive lock recipe: create guid-lock- sequential ephemeral node, check lowest suffix, watch the predecessor, and recover from failed creates."
sources:
  - https://zookeeper.apache.org/doc/current/recipes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed lock

Acquire (lock node `locknode`):
1. `create()` `locknode/guid-lock-` with SEQUENCE and EPHEMERAL.
2. `getChildren()` on `locknode` without a watch.
3. If your node has the lowest suffix, you hold the lock.
4. Otherwise `exists()` with a watch on the node with the next-lowest number.
5. If `exists()` returns null go to step 2; else wait for the notification, then step 2.

Release: delete your node.

Properties: each release wakes one client, no polling or timeouts, and contention is visible in the children. If `create()` fails recoverably, `getChildren()` and look for a node containing your GUID.

Verify: with two clients, the second blocks until the first deletes its node or its session ends.

## Checked

Confirmed against the ZooKeeper Recipes page: lock protocol steps, release by deleting the node, listed properties, and GUID recovery after a recoverable create error. No changes needed.

Method: docs-only read of cited pages, 2026-11-08
