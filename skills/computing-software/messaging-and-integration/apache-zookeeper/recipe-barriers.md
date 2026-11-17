---
id: computing-software.messaging-and-integration.apache-zookeeper.recipe-barriers
name: recipe-barriers
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, recipes, barrier, double-barrier, synchronization, watches]
level: practitioner
status: docs-checked
description: "ZooKeeper barrier recipes: simple barrier with exists watch and the double barrier enter/leave protocol using a ready node."
sources:
  - https://zookeeper.apache.org/doc/current/recipes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Barriers

Simple barrier: `exists()` on the barrier node with watch true; if false proceed; if true wait for the event and repeat.

Double barrier (barrier node `b`, process node `b/p`, ready node `b/ready`, threshold x):
- Enter: set watch `exists(b/ready, true)`; create `b/p` as EPHEMERAL; `getChildren(b, false)`; if fewer than x children wait, else create `b/ready` (regular) to wake everyone.
- Leave: `getChildren(b)`; if none, exit; if you are the only one, delete your node and exit; if you are the lowest, wait on the highest; otherwise delete yours and wait on the lowest; loop.
- The lowest node acts as the ready flag, so each deletion wakes one process except the last.

Verify: with x processes started, none passes enter until the x-th arrives.

## Checked

Confirmed against the ZooKeeper Recipes page: simple barrier exists() loop and the double barrier Enter and Leave steps, including the lowest-node efficiency note. No changes needed.

Method: docs-only read of cited pages, 2026-11-08
