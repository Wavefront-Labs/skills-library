---
id: computing-software.database-administration.scylladb.kb-seed-nodes
name: kb-seed-nodes
category: computing-software
field: database-administration
product: scylladb
tags: [seeds, scylla-yaml, gossip, cluster-join, bootstrap]
level: practitioner
status: docs-checked
description: "What ScyllaDB seed nodes do: first contact for joining nodes to learn ring topology, no role after joining, first node must be a seed, one seed usually enough."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/seed-nodes.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Seed nodes

A seed node is a node listed in the `seeds` parameter of `scylla.yaml`. A node that is joining the cluster uses it as the first contact point, so it can learn the ring topology on startup:
- the IP addresses of the nodes in the cluster,
- which token ranges are available,
- which nodes will own which tokens once the new node joins.

**Once the nodes have joined the cluster, the seed node has no function.** It is not a coordinator or leader and gets no special treatment after bootstrap.

Rules from the docs:
- The first node in a new cluster must be a seed node.
- In typical scenarios there is no need to configure more than one seed node.

## Checked

2026-11-04. Confirmed against kb/seed-nodes.rst: seeds parameter, first contact, the three topology items, no function after joining, first node must be a seed, one seed usually enough. Removed the practical-consequences bullets and the example setting, which the page does not give.

Method: documentation only; no commands were run.
