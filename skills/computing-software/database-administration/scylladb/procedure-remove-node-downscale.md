---
id: computing-software.database-administration.scylladb.procedure-remove-node-downscale
name: procedure-remove-node-downscale
category: computing-software
field: database-administration
product: scylladb
tags: [downscale, decommission, removenode, rf-rack-valid, cluster-repair]
level: practitioner
status: docs-checked
description: "Remove a node from a ScyllaDB cluster: decommission for running nodes, joining and down node cases, repair before removenode, RF-rack-valid warning, and data cleanup."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/remove-node.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/safely-removing-joining-node.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remove a node (down scale)

Start with `nodetool status` and branch on node state.

**UN (running)**: run `nodetool decommission` on the node to remove. This is the recommended scale-down method because the node streams its data to the rest, preventing data loss. Watch `nodetool netstats`, then confirm with `nodetool status`. Afterwards, delete the node data and commit log yourself; they are not removed automatically.

**Joining (UJ)**: a node stuck joining that never reached UN can be wiped: `nodetool drain`, stop the service, clean the data, start again.

**DN (down)**: try to restore it first and then decommission. If it is permanently dead, use `nodetool removenode <Host ID>` as a fallback; never on a node other nodes can reach. removenode asks others to redistribute the range by streaming and does not guarantee consistency if sources lack the latest data, and it fails if other nodes are unavailable. To make it succeed consistently:
- all other nodes must be `UN` (otherwise use `--ignore-dead-nodes`);
- run a full cluster repair before removenode so replicas are current;
- if nodes fail during removenode, repair again before retrying (unneeded when RBNO is on for removenode).

Warning: removing a node from a rack may violate RF-rack-valid constraints. For tablet keyspaces with a materialized view or secondary index, or when `rf_rack_valid_keyspaces` is set, the removal is rejected if it would break the invariant.

## Checked

2026-11-04. Confirmed against remove-node.rst and safely-removing-joining-node.rst: UN, UJ and DN branches, decommission as recommended method, netstats and status, data cleanup, removenode warnings and the three consistency steps, RF-rack-valid warning. Nothing removed.

Method: documentation only; no commands were run.
