---
id: computing-software.messaging-and-integration.apache-zookeeper.recipe-shared-and-revocable-locks
name: recipe-shared-and-revocable-locks
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, recipes, read-write-lock, shared-lock, revocable-lock, unlock]
level: advanced
status: docs-checked
description: "ZooKeeper read/write shared locks using read- and write- sequential nodes, why reader wake-ups are not a herd, and revocable locks via an unlock write."
sources:
  - https://zookeeper.apache.org/doc/current/recipes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared and revocable locks

Read lock:
1. Create `guid-/read-` (SEQUENCE and EPHEMERAL).
2. `getChildren()` without a watch.
3. No `write-` child with a lower number means you hold it.
4. Else `exists()` with watch on the nearest lower `write-` node; if absent repeat step 2, otherwise wait.

Write lock: create `guid-/write-`; same loop, but you hold it only when no child has a lower number; watch the next-lowest node.

Herd note: many readers waking after a writer releases is correct since all can proceed.

Revocable: after `create()` the holder calls `getData()` with watch; on notification it re-reads and looks for "unlock". A revoker calls `setData()` writing "unlock". Release is by consent; a revoker may delete the node after a timeout.

Verify: concurrent readers all proceed, and a writer waits for all lower-numbered nodes.

## Checked

Confirmed against the ZooKeeper Recipes page: read and write lock steps, why waking many readers is not a herd, revocable locks via getData watch and an unlock write, consent-based release. No changes needed.

Method: docs-only read of cited pages, 2026-11-08
