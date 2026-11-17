---
id: computing-software.database-administration.scylladb.nodetool-excludenode
name: nodetool-excludenode
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, excludenode, dead-node, tablets, topology]
level: advanced
status: docs-checked
description: "nodetool excludenode: mark a permanently dead node as excluded to unblock tablet load balancing and replication changes, effects, prerequisites and relation to removenode."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/excludenode.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool excludenode

`nodetool excludenode <Host ID>` marks nodes as permanently down. Never use it on a running node that other nodes can reach; make sure the node is dead and cannot be recovered first.

Effects:
- The cluster stops trying to contact excluded nodes, which unblocks operations such as tablet load balancing and replication changes.
- Excluded nodes are banned permanently; they cannot be brought back.
- Data ownership does not change and the nodes remain cluster members, so you must still remove them (`nodetool removenode`) or replace them eventually.
- After exclusion you no longer need to list them as ignored nodes for removenode, replace or repair.

Prerequisite: a quorum of nodes must be available.

```
nodetool excludenode <Host ID of the dead node>
```

Several Host IDs may be given in one command. To remove the node rather than only mark it down, run `nodetool removenode`, which bans the node itself at the start of the procedure.

## Checked

2026-11-04. Confirmed against nodetool-commands/excludenode.rst and removenode.rst: warning, effects, permanent ban, quorum prerequisite, syntax with several Host IDs, and that removenode bans the node. Removed the use-case advice not in the page.

Method: documentation only; no commands were run.
