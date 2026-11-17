---
id: computing-software.database-administration.scylladb.nodetool-cleanup
name: nodetool-cleanup
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, cleanup, scale-out, token-ranges, disk-space]
level: practitioner
status: docs-checked
description: "When and how to run nodetool cleanup after scale-out: removes data a node no longer owns, per-keyspace usage, no need after permanent removal, and the all-nodes-UN precondition."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/cleanup.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool cleanup

`nodetool cleanup [<keyspace> <tablename ...>]` immediately deletes data from nodes that "lose" part of their token range due to a range movement (node addition or replacement).

When to run it: after scaling out, when new nodes joined the same DC. The token ring is redistributed, so some existing nodes still hold replicas for tokens they no longer own. That data keeps using disk until cleanup removes it.

Rules of thumb:
- Optionally restrict by keyspace and table. With no keyspace, all keyspaces are cleaned.
- No need to run cleanup when nodes are removed permanently.
- Make sure no topology change is in flight: `nodetool status` must show every node `UN` (Up Normal) before you start.

Single node and keyspace:

```
nodetool -h <host name> cleanup <keyspace>
```

To clean the whole cluster use `nodetool cluster cleanup`.

## Checked

2026-11-04. Confirmed against nodetool-commands/cleanup.rst: purpose, when to run after scale-out, optional keyspace and table, all keyspaces by default, not needed when nodes are removed, nodetool -h example, nodetool cluster cleanup, UN warning. Removed the unsupported advice to run only on existing nodes and the operational resource paragraph.

Method: documentation only; no commands were run.
