---
id: computing-software.database-administration.scylladb.procedure-add-datacenter
name: procedure-add-datacenter
category: computing-software
field: database-administration
product: scylladb
tags: [add-datacenter, rebuild, network-topology-strategy, snitch, local-consistency]
level: advanced
status: docs-checked
description: "Add a data center to a live ScyllaDB cluster: LOCAL_* consistency first, clean nodes, NetworkTopologyStrategy, snitch and rackdc settings, ALTER KEYSPACE, rebuild, repair."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/add-dc-to-existing-dc.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Add a data center to an existing cluster

Complete the whole procedure before reading from the new DC; by default it would be used for reads.

Prerequisites:
- Collect cluster info from an existing node; `cluster_name`, `seeds` and `endpoint_snitch` on the new nodes must match the existing cluster.
- Switch all clients to `LOCAL_*` consistency (`LOCAL_ONE`, `LOCAL_QUORUM`) so coordinators do not touch the new DC yet.
- New nodes must be clean (no data) or you risk data loss; if one started during installation, follow the page's clear-data instructions.
- All keyspaces must use `NetworkTopologyStrategy` (otherwise convert them first).

Procedure:
1. On existing nodes set `endpoint_snitch` to `Ec2MultiRegionSnitch` (AWS) or `GossipingPropertyFileSnitch` (elsewhere).
2. In `/etc/scylla/cassandra-rackdc.properties` set `dc` and `rack` (GossipingPropertyFileSnitch), or `dc_suffix` for Ec2MultiRegionSnitch (region `us-east` with `dc_suffix=_1_scylla` becomes `us-east_1_scylla`).
3. Configure the new nodes with the same `cluster_name`, seeds and snitch, start them one by one, and verify with `nodetool status`.
4. `ALTER KEYSPACE` for each keyspace to add the new DC with its RF, including the system_distributed, system_traces and audit keyspaces.
5. If any vnode keyspace was altered, run `nodetool rebuild <existing-dc-name>` on each new node.
6. If any vnode keyspace was altered, run a full cluster repair (`nodetool repair -pr` on each node, or ScyllaDB Manager); update the monitoring stack, then switch clients as desired.

## Checked

2026-11-04: prerequisites, snitch choices, rackdc settings, dc_suffix example, ALTER KEYSPACE step, rebuild and repair confirmed against the ScyllaDB add-a-data-center procedure page. Removed the unsupported quorum prerequisite and the version and commitlog details; the page limits rebuild and repair to vnode keyspaces.

Method: documentation only; no commands were run.
