---
id: computing-software.database-administration.scylladb.repair-based-node-operations
name: repair-based-node-operations
category: computing-software
field: database-administration
product: scylladb
tags: [rbno, repair, bootstrap, decommission, removenode, configuration]
level: advanced
status: docs-checked
description: "Repair Based Node Operations (RBNO): why it is safer and resumable, covered operations, and the enable_repair_based_node_ops and allowed_repair_based_node_ops settings."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/repair-based-node-operation.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repair Based Node Operations (RBNO)

Data moves between nodes during topology changes (add or remove a node) and during repair. By default ScyllaDB uses the row-level repair mechanism for node operations instead of plain streaming; this is RBNO.

Benefits:
- More robust and safer for data consistency than streaming.
- A failed node operation resumes from where it stopped, without resending data already synced: a large time saver when adding or removing big nodes.
- You do not need to run repair before or after replace or removenode when RBNO is on.

RBNO covers: bootstrap, decommission, rebuild, removenode, replace.

Configuration in `scylla.yaml`:
- `enable_repair_based_node_ops: true|false` turns RBNO on or off.
- `allowed_repair_based_node_ops: "replace,removenode,rebuild,bootstrap,decommission"` specifies the node operations for which RBNO is enabled.

Example restricting RBNO to replace and removenode:

```
allowed_repair_based_node_ops: "replace,removenode"
```

Remember that rebuild under RBNO reads all source replicas per token range and repairs discrepancies, while without RBNO it streams from a single source replica. `nodetool rebuild` works only for vnode keyspaces; for tablet keyspaces use `nodetool cluster repair`. See the configuration parameters reference for details.

## Checked

2026-11-04. Confirmed against repair-based-node-operation.rst and rebuild.rst: RBNO definition, benefits, covered operations, the two options, rebuild behaviour with and without RBNO, vnode-only rebuild. Removed the claim that RBNO settings only concern vnode operations and the fall-back-to-streaming wording.

Method: documentation only; no commands were run.
