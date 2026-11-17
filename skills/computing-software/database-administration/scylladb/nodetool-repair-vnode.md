---
id: computing-software.database-administration.scylladb.nodetool-repair-vnode
name: nodetool-repair-vnode
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, repair, vnodes, gc-grace-seconds, partitioner-range]
level: practitioner
status: docs-checked
description: "nodetool repair options for vnode keyspaces: -pr, -local, -dc, -hosts, token ranges, schedule against gc_grace_seconds, and why not to repair during topology changes."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/repair.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool repair (vnode keyspaces)

`nodetool repair` synchronises replicas in the background. The node you run it on is the repair master: only its data subset (and the replicas of that subset) is repaired, so to cover the cluster you repair every node, or let ScyllaDB Manager schedule it. This command only repairs keyspaces with tablets disabled; check with `DESCRIBE KEYSPACE ks`.

Schedule: if you delete data, repair more often than `gc_grace_seconds` (default 10 days), for example weekly, running `nodetool repair -pr` on each node sequentially.

Options:
- `-pr` / `--partitioner-range`: only the primary replica returned by the partitioner.
- `-local` / `--in-local-dc`: nodes in the local DC only.
- `-dc <dc>` / `--in-dc`: nodes in one DC, which must be the repair master's DC; leaves other DCs out of sync.
- `-hosts` / `--in-hosts`: comma-separated host IDs or addresses; must include the master; others stay unsynced.
- `-st` / `--start-token`, `-et` / `--end-token`: restrict to a token range.
- Positional `keyspace [table ...]`; default is all keyspaces and tables.

```
nodetool repair -pr my_keyspace my_table
nodetool repair --in-hosts 172.17.0.2,172.17.0.3,172.17.0.4
```

Mixed clusters (tablet and vnode keyspaces): run `nodetool repair -pr` on all nodes and `nodetool cluster repair` on any one node.

Warning: do not run maintenance operations (add, remove, decommission, replace, rebuild) or schema changes (CREATE/DROP/TRUNCATE/ALTER) while repairs run; they are likely to make the repair fail.

## Checked

2026-11-04: options, the vnode-only scope, mixed-cluster advice, the gc_grace_seconds schedule note and the maintenance warning confirmed against the ScyllaDB nodetool repair documentation page. Removed the unsupported explanation of why to use -pr on every node.

Method: documentation only; no commands were run.
