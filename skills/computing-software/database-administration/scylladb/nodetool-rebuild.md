---
id: computing-software.database-administration.scylladb.nodetool-rebuild
name: nodetool-rebuild
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, rebuild, rbno, new-datacenter, streaming]
level: practitioner
status: docs-checked
description: "nodetool rebuild: stream data from another DC or replicas, source-dc argument, --force, repair-based rebuild, and vnode-only limit; used when adding a data center."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/rebuild.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool rebuild

`nodetool rebuild [[--force] <source-dc-name>]` rebuilds a node's data by streaming from other nodes, similar to bootstrap. ScyllaDB works out which token ranges the local node owns, then finds nodes holding the same ranges.

Source selection:
- With `source-dc-name`, data is streamed only from that datacenter when it is safe to do so.
- Without it, an alternative datacenter that lost no nodes is considered; if none exist, all datacenters are considered.
- `--force` forces the named source DC even when that is unsafe.

If rebuild is enabled in Repair Based Node Operations (RBNO), it reads all source replicas of each token range and repairs any discrepancies. Otherwise each range is streamed from a single source replica.

Use rebuild when adding a new datacenter to an existing cluster:

```
nodetool rebuild <source-dc-name>
```

Notes:
- The rebuild keeps running in the background if the nodetool process is killed or interrupted.
- It works only for vnode keyspaces. For tablet keyspaces use `nodetool cluster repair` instead.

## Checked

2026-11-04. Confirmed against nodetool-commands/rebuild.rst: synopsis, source datacenter selection, --force, RBNO behaviour, new datacenter use, background execution, vnode-only note. Removed the unsupported concurrency advice and the per-node timing parenthetical.

Method: documentation only; no commands were run.
