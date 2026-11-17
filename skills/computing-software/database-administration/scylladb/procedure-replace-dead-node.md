---
id: computing-software.database-administration.scylladb.procedure-replace-dead-node
name: procedure-replace-dead-node
category: computing-software
field: database-administration
product: scylladb
tags: [replace-node, dead-node, replace-node-first-boot, gossipinfo, bootstrap]
level: advanced
status: docs-checked
description: "Replace a dead ScyllaDB node: verify DN status, quorum, collect cluster info, set replace_node_first_boot to the old Host ID in scylla.yaml, and watch progress with gossipinfo."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/replace-dead-node.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/replace-dead-node-or-more.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replace a dead node

Other nodes stream data to the replacement, which can take a while. Quorum must be available (restore it first if not). You can replace several dead nodes in parallel.

Prepare:
- `nodetool status`: the node to replace must be `DN`. Note its Host ID.
- If you can, log in to the dead node and delete its data.
- On a healthy node collect `cluster_name`, `seeds`, `endpoint_snitch` (grep `/etc/scylla/scylla.yaml`) and `scylla --version`.

Procedure:
1. Install the identical ScyllaDB version on the new node, stopping before configuration.
2. In `/etc/scylla/scylla.yaml` set `cluster_name`, `listen_address`, `seeds`, `endpoint_snitch`, `rpc_address`.
3. Add the parameter with the failed node Host ID anywhere in the file; it can stay after success:
   `replace_node_first_boot: 675ed9f4-6564-6dbd-ca08-43fddce952de`
   (the older replace_address options are obsolete).
4. Start the node.
5. During bootstrap the new node does not appear in `nodetool status`; use `nodetool gossipinfo` and look for `STATUS:NORMAL` on its entry (the dead node shows `STATUS:shutdown,true`). Afterwards status shows the new node `UN` and the old one gone.

More than one dead node: if the number of failed nodes is smaller than the keyspace RF, at least one replica survives and you use the same procedure per node. If it is equal or larger, some data is lost and must be restored from backup after replacing.

## Checked

2026-11-04. Confirmed against replace-dead-node.rst and replace-dead-node-or-more.rst: parallel replacement, quorum, DN check, data removal, information to collect, procedure steps, replace_node_first_boot and obsolete options, gossipinfo check, RF rule for several dead nodes. Nothing removed.

Method: documentation only; no commands were run.
