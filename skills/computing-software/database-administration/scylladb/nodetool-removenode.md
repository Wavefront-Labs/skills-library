---
id: computing-software.database-administration.scylladb.nodetool-removenode
name: nodetool-removenode
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, removenode, excludenode, ignore-dead-nodes, quorum]
level: advanced
status: docs-checked
description: "nodetool removenode for permanently dead nodes: never use on reachable nodes, banning semantics, quorum and RF prerequisites, --ignore-dead-nodes, excludenode, parallel use."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/removenode.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool removenode

Use `nodetool removenode <Host ID>` only when the node is Down Normal (`DN`) and every attempt to restore it has failed. Never use it on a node other nodes can reach; use `nodetool decommission` there.

The target node and any ignored dead nodes are permanently banned at the start of the procedure. They cannot rejoin even if removenode fails, and until the banned node is removed or replaced you cannot run other topology operations such as decommission or bootstrap.

Prerequisites:
- A quorum of nodes must be available; restore quorum first (see the handling-node-failures skill).
- Nodes remaining in each DC must be at least that DC's RF. If not, replace the dead node instead of removing it.

```
nodetool removenode 675ed9f4-6564-6dbd-ca08-43fddce952de
nodetool removenode --ignore-dead-nodes <hostid1>,<hostid2> <hostid-to-remove>
```

All nodes take part in syncing data, so the operation fails if other nodes are down; list every unavailable node in `--ignore-dead-nodes` (comma-separated host IDs, before the node to remove).

`nodetool excludenode <Host ID>` only marks a node permanently down without doing the removal.

Parallel runs are allowed: tablets of removed nodes are rebuilt in parallel, while the vnode part is serialised. A removenode still in the tablet rebuild phase can be cancelled via Task Manager; already rebuilt tablets stay on their new replicas.

## Checked

2026-11-04. Confirmed against nodetool-commands/removenode.rst: DN and last-resort warning, permanent ban, quorum and RF prerequisites, usage and --ignore-dead-nodes, excludenode, parallel runs and Task Manager cancellation. Nothing removed.

Method: documentation only; no commands were run.
