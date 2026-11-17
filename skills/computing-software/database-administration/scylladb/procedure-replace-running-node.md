---
id: computing-software.database-administration.scylladb.procedure-replace-running-node
name: procedure-replace-running-node
category: computing-software
field: database-administration
product: scylladb
tags: [replace-node, decommission, drain, rf, vnodes]
level: advanced
status: docs-checked
description: "Two ways to replace a healthy ScyllaDB node: add then decommission (safe, double streaming) versus drain, stop and take its place (efficient, temporarily reduced replication)."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/replace-running-node.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replace a running node

Two methods; both need a quorum of nodes available.

**1. Add a new node, then decommission the old one**
- Keeps the full replication level the whole time, but moves more data: vnodes are redistributed twice, and a node worth of data is streamed each time.
- Steps: follow the add-node procedure; decommission the old node using the remove-node procedure; run `nodetool cleanup` on all remaining nodes; confirm with `nodetool status`.

**2. Take its place in the cluster**
- Less safe, since the replication factor is temporarily reduced, but more efficient: vnode distribution does not change and only one node worth of data is streamed.
- Steps:
  1. `nodetool drain` on the node to replace (it stops listening to clients and other nodes).
  2. Stop the ScyllaDB service on that node.
  3. Follow the replace-a-dead-node procedure, using the stopped node Host ID in `replace_node_first_boot`.
  4. Confirm with `nodetool status`.

Method 1 keeps the replication level throughout at the cost of more data transferred; method 2 is more efficient but temporarily reduces the replication factor.

## Checked

2026-11-04. Confirmed against replace-running-node.rst: both methods, vnode and streaming trade-offs, steps for each. Removed the unsupported guidance on when to choose each method.

Method: documentation only; no commands were run.
