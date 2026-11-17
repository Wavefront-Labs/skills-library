---
id: computing-software.database-administration.cassandra.gossip-protocol
name: gossip-protocol
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, gossip-protocol, phi-accrual, failure-detector, gossip, token-ring, dynamo-architecture, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Reading gossipinfo, seeds and the phi-accrual failure detector"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gossip and failure detection

Goal: understand how nodes learn cluster state.
- Every second each node updates its own heartbeat state, gossips with one random other node, probabilistically gossips with an unreachable node, and gossips with a seed node if it did not in the random step.
- Gossip carries membership, internode protocol versions, token metadata and schema version, versioned as `(generation, version)`.
- Seeds differ only in being allowed to bootstrap without seeing another seed; they become gossip hotspots. Non-seed nodes must reach at least one seed to join, so use several, often one per rack or datacenter; nodes need not agree on the list.
- Liveness comes from a failure detector based on gossip.
Verify: all nodes see each other as UN in `nodetool status`.

## Checked

2026-11-02. Checked against the Dynamo architecture page (Gossip section, seeds, failure detection). Removed: 'up to 3 peers', `phi_convict_threshold` default 8 and the 10-12 flapping advice, '2-3 seeds per datacenter, same list everywhere' (the docs say nodes need not agree), and the `nodetool gossipinfo` field list (no reference page).

Method: documentation only; no commands were run.
