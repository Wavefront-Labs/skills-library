---
id: computing-software.database-administration.scylladb.procedure-add-node
name: procedure-add-node
category: computing-software
field: database-administration
product: scylladb
tags: [add-node, bootstrap, scylla-yaml, cleanup, scale-out]
level: practitioner
status: docs-checked
description: "Add a node to a ScyllaDB cluster: prerequisites, scylla.yaml parameters, UJ to UN monitoring, RF-rack-valid warning, and running cleanup on the other nodes afterwards."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/add-node-to-cluster.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Add a node to an existing cluster (scale out)

Bootstrapping streams data from existing nodes to the new one and can take a long time depending on data size and bandwidth. You cannot add nodes while any existing node is down: check `nodetool status` first. With multiple availability zones, keep them balanced.

Steps:
1. Install the same ScyllaDB version as the cluster, stopping before `scylla.yaml` configuration. If the node starts automatically, clear its data first.
2. Edit `/etc/scylla/scylla.yaml` on the new node: `cluster_name`, `listen_address` (inter-node address), `endpoint_snitch`, `rpc_address` (CQL clients) and `seeds` (an existing node IP used to learn topology).
3. Start the node.
4. Run `nodetool status` on another node. The new node shows `UJ` (Up Joining) while streaming; wait for `UN`.
5. When `UN`, run `nodetool cleanup` on every node except the new one, to drop keys now owned by the new node.
6. Update ScyllaDB Monitoring targets and install the Manager Agent if you use Manager.

Warning: adding a node in a new rack of an existing DC can violate the RF-rack-valid constraint. If a tablet keyspace has a materialized view or secondary index, or `rf_rack_valid_keyspaces` is set, the new node is rejected when it would break the invariant.

Cleanup guidance: finish cleanup before any node is decommissioned or removed (prevents data resurrection). When adding several nodes, run cleanup after all are added, on all but the last added; schedule it in low-demand hours; run it one node at a time.

## Checked

2026-11-04. Confirmed against cluster-management/add-node-to-cluster.rst and clear-data.rst: bootstrapping, no nodes down, install steps, the five scylla.yaml parameters, UJ to UN, cleanup on all nodes except the new one, cleanup tips, RF-rack-valid warning, Monitoring and Manager Agent step. Nothing removed.

Method: documentation only; no commands were run.
