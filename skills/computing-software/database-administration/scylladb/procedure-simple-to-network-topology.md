---
id: computing-software.database-administration.scylladb.procedure-simple-to-network-topology
name: procedure-simple-to-network-topology
category: computing-software
field: database-administration
product: scylladb
tags: [simplestrategy, network-topology-strategy, replication, alter-keyspace, snitch]
level: advanced
status: docs-checked
description: "Convert keyspaces from SimpleStrategy to NetworkTopologyStrategy: which keyspaces to check, no-downtime criteria, the full-shutdown procedure with two repairs, and snitch change."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/update-topology-strategy-from-simple-to-network.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SimpleStrategy to NetworkTopologyStrategy

SimpleStrategy is not recommended in production. Check user keyspaces (`DESCRIBE SCHEMA`) and the system keyspaces `system_distributed`, `system_traces` and `system_audit` (`DESCRIBE KEYSPACE system_traces;`).

**No downtime** is allowed when either all nodes are on the same rack, or the SimpleStrategy RF is not changing and equals the number of nodes (for example RF 3 on 3 nodes). Then:

```
ALTER KEYSPACE mykeyspace WITH replication = {'class':'NetworkTopologyStrategy','<existing_dc>':3};
```
Finish by changing the snitch and setting the preferred DC name in `cassandra-rackdc.properties`.

**With downtime** (a full shutdown of the cluster) is required when nodes sit on multiple racks and either the RF is not equal to the node count (and not changing) or the RF is changing, because the new strategy may select different replicas. Steps, with all client traffic stopped:
1. Stop all traffic. Failing to do so can cause data loss.
2. Run a full repair on the cluster.
3. Alter the strategy as above.
4. Run a second full repair.
5. Run `nodetool cleanup` on each node.
6. Resume traffic.

Use `nodetool status` to see which node is on which rack. Then switch the snitch and edit `cassandra-rackdc.properties` as in the no-downtime path.

## Checked

2026-11-04. Confirmed against update-topology-strategy-from-simple-to-network.rst: keyspaces to check, no-downtime and downtime conditions, ALTER example, steps and snitch follow-up. Added that the downtime path is a full cluster shutdown.

Method: documentation only; no commands were run.
