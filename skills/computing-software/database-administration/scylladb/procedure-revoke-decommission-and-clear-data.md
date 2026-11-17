---
id: computing-software.database-administration.scylladb.procedure-revoke-decommission-and-clear-data
name: procedure-revoke-decommission-and-clear-data
category: computing-software
field: database-administration
product: scylladb
tags: [decommission, clear-data, node-restart, bootstrap, commitlog]
level: practitioner
status: docs-checked
description: "Re-add a decommissioned node (wipe data and commitlog, join as new) and recover when a node started before configuration: stop, clean data, start, verify with nodetool status."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/revoke-decommission.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/clear-data.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Re-add a decommissioned node and handle an accidental start

**Node started before configuration**: if ScyllaDB ran before you edited `scylla.yaml`, some system tables already hold wrong state and a restart will not fix it. The safe route:
1. Stop the ScyllaDB service.
2. Delete the data and commitlog directories.
3. Start the service.
4. Run `nodetool status` to check every node is up and joined.

**Decommissioned by mistake**: a decommissioned node cannot simply be restarted. It is added back as a brand new node:
1. Confirm `nodetool status` no longer lists it.
2. Stop the node.
3. Delete the data and commitlog folders. This is mandatory: old state such as the bootstrap status would otherwise prevent the node from starting its initialisation.
4. Follow the add-a-node procedure (same `scylla.yaml` settings, start, wait for `UN`, then `nodetool cleanup` on the other nodes).

Both cases delete the data and commitlog before starting. A node stuck in `UJ` that never reached `UN` is handled the same way (drain, stop, clean, start), per the safely-remove-a-joining-node page.

## Checked

2026-11-04. Confirmed against revoke-decommission.rst, clear-data.rst and safely-removing-joining-node.rst: both procedures and the reason for deleting data. Reworded the closing rule to what the pages state.

Method: documentation only; no commands were run.
