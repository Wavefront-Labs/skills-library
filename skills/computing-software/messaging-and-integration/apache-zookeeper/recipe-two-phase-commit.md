---
id: computing-software.messaging-and-integration.apache-zookeeper.recipe-two-phase-commit
name: recipe-two-phase-commit
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, recipes, two-phase-commit, coordinator, transaction-node, voting]
level: advanced
status: docs-checked
description: "Two-phase commit on ZooKeeper: coordinator creates /app/Tx with per-site children, sites vote commit or abort, drawbacks and the coordinator-only watch mitigation."
sources:
  - https://zookeeper.apache.org/doc/current/recipes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-phase commit recipe

1. Coordinator creates a transaction node (e.g. `/app/Tx`) and one child per site (`/app/Tx/s_i`) with undefined content.
2. Each site reads its child, sets a watch, processes the query and votes commit or abort by writing to its own node.
3. Sites decide once all votes are in; one abort allows early abort.

Coordinator selects sites, creates nodes and propagates the transaction (may be written into the transaction node).

Drawbacks: message complexity O(n squared); ephemeral nodes cannot detect site failure unless the site creates the node itself.

Mitigations: only the coordinator watches transaction nodes (scales better, slower since all traffic goes through it); sites create their own ephemeral nodes so failure is detectable.

Verify: one site writing abort causes all sites to see abort.

## Checked

Confirmed against the ZooKeeper Recipes page: transaction node with per-site children, voting by writing to own node, early abort, O(n squared) message cost, the ephemeral-node failure detection limit and both mitigations. No changes needed.

Method: docs-only read of cited pages, 2026-11-08
