---
id: computing-software.messaging-and-integration.apache-zookeeper.recipe-queues
name: recipe-queues
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, recipes, queue, priority-queue, producer-consumer, sequential]
level: practitioner
status: docs-checked
description: "ZooKeeper queue recipes: producers create queue-X sequential nodes, consumers take the lowest, and priority queues named queue-YY."
sources:
  - https://zookeeper.apache.org/doc/current/recipes.html
  - https://zookeeper.apache.org/doc/current/zookeeperTutorial.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queues

- Producer: `create()` a path ending `queue-` with SEQUENCE and EPHEMERAL, giving `queue-node/queue-X` with X increasing.
- Consumer: `getChildren()` on the queue node with a watch; process the lowest-numbered node; re-list only after the list is exhausted; if empty wait for the watch.
- Priority queue: names `queue-YY`, lower YY = higher priority; discard the cached list when the watch fires.
- Tutorial variant: PERSISTENT_SEQUENTIAL children named "element"; `getChildren()` is lexicographic, so parse the numeric suffix; contending consumers see a failed delete and retry.

Verify: two consumers never both process the same element.

## Checked

Confirmed against the ZooKeeper Recipes page (queue and priority queue) and the Tutorial page (PERSISTENT_SEQUENTIAL children named element, lexicographic getChildren order, failed delete under contention). No changes needed.

Method: docs-only read of cited pages, 2026-11-08
