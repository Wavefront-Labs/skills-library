---
id: computing-software.database-administration.cassandra.decommission-and-replace
name: decommission-and-replace
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, removenode, replace-address, assassinate, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Removing or swapping nodes"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/topo_changes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decommission, removenode and replace

Goal: remove a live or dead node correctly.
- Live node: `nodetool decommission` streams its data out. Dead node: `nodetool removenode` from any other machine streams from the remaining replicas.
- Replace a dead node by starting the new one with `-Dcassandra.replace_address_first_boot=<dead_node_ip>`; it hibernates (others see it DOWN) and `nodetool netstats` shows the real state.
- You must run repair afterwards if the node was down longer than `max_hint_window` before replacement, or if you replace using the same IP and replacement takes longer than `max_hint_window`.
- No data is removed from a decommissioned node automatically.
Verify: `nodetool status` shows no DN for the removed node.

## Checked

2026-11-02. Checked against Adding, replacing, moving and removing nodes (decommission, removenode, replace_address_first_boot, hibernate state, repair conditions). Removed: `nodetool assassinate` (no page in the docs repo) and the 'confirm for your version' hedge.

Method: documentation only; no commands were run.
