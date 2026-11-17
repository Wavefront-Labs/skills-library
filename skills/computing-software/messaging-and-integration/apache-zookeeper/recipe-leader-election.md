---
id: computing-software.messaging-and-integration.apache-zookeeper.recipe-leader-election
name: recipe-leader-election
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, recipes, leader-election, election-node, predecessor-watch, ephemeral-sequential]
level: practitioner
status: docs-checked
description: "Application-level leader election on ZooKeeper: ELECTION/guid-n_ nodes, smallest sequence leads, watch only the predecessor, and an optional ack node."
sources:
  - https://zookeeper.apache.org/doc/current/recipes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leader election recipe

Node `ELECTION`:
1. Each volunteer creates `ELECTION/guid-n_` with SEQUENCE and EPHEMERAL.
2. Let C be the children and i your sequence number.
3. Watch `ELECTION/guid-n_j` where j is the largest sequence number below i.

On a deletion notification: re-fetch C; if you are smallest, run the leader procedure; otherwise watch the next-lower node.

The smallest sequence is the leader. Watching only the predecessor avoids a herd. Having no predecessor does not prove the leader finished setup, so applications may add a separate acknowledgment node.

Verify: killing the leader's session promotes exactly the next-lowest candidate.

## Checked

Confirmed against the ZooKeeper Recipes page: ELECTION/guid-n_ with SEQUENCE and EPHEMERAL, smallest sequence leads, watch the next znode down, and the optional acknowledgment znode. No changes needed.

Method: docs-only read of cited pages, 2026-11-08
