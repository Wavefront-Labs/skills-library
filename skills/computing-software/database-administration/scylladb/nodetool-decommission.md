---
id: computing-software.database-administration.scylladb.nodetool-decommission
name: nodetool-decommission
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, decommission, downscale, tablets, task-manager]
level: practitioner
status: docs-checked
description: "nodetool decommission prerequisites and behaviour: disk headroom on remaining nodes, RF vs remaining nodes, audit keyspace, parallel decommission, cancelling in the tablet phase."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/decommission.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool decommission

`nodetool decommission` deactivates the node it runs on by streaming its data to the next node in the ring. Monitor token reallocation with `nodetool netstats`. You cannot decommission while any existing node is down.

Check before running:
- Disk: the data streamed from the leaving node must fit on the remaining nodes; otherwise the removal fails. Add storage first.
- Replication factor: nodes remaining in the DC must be at least the RF of every keyspace in that DC. The `audit` keyspace (audit is enabled by default) may need its RF altered, as do user keyspaces; ALTER the keyspace to lower RF before decommissioning, or the request may fail.

Parallelism: you may decommission several nodes at once. With tablet-based keyspaces this is faster because tablets are migrated off in parallel. The vnode part of decommission is serialised with other vnode-based operations, including other decommissions.

Cancellation: a decommission still in the tablet draining phase can be cancelled using the Task Manager API; see the task-manager skill.

If it fails, see the failed-decommission troubleshooting page; related procedures are removing a node (down-scale), decommissioning a whole DC and replacing a running node.

## Checked

2026-11-04. Confirmed against nodetool-commands/decommission.rst: streaming to the next node in the ring, netstats, no decommission with a down node, disk and RF checks, audit keyspace, parallel decommission, Task Manager cancellation, related pages. Corrected the streaming target and removed the unsupported removenode aside.

Method: documentation only; no commands were run.
