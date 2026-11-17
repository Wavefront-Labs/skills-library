---
id: computing-software.database-administration.cassandra.bootstrap-new-node
name: bootstrap-new-node
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, bootstrap-node, auto-bootstrap, join-ring, bootstrap, decommission, replace-node, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Adding capacity"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/topo_changes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrapping a node

Goal: add nodes without outages.
- `num_tokens` sets how many vnodes the joining node is assigned; the new node streams its ranges from the cluster.
- Watch progress with `nodetool netstats`.
- Cassandra does not remove data from nodes that lose ranges: once the new node works, run `nodetool cleanup` on the nodes that lost ranges, or the old data still counts against their load.
- `auto_bootstrap: false` skips bootstrap and is for restoring a node from a backup or creating a new data-center.
Verify: the node shows UN and cleanup completes.

## Checked

2026-11-02. Checked against Adding, replacing, moving and removing nodes (bootstrap, num_tokens, netstats, cleanup after range movements, auto_bootstrap: false). Removed: the list of settings to set before starting, the 'one node at a time' rule and the UJ state (not stated in the pages).

Method: documentation only; no commands were run.
