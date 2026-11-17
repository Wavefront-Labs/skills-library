---
id: computing-software.data-engineering.apache-pinot.apache-pinot-instance-assignment-config
name: apache-pinot-instance-assignment-config
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, instance-assignment, instanceassignmentconfigmap, tagpoolconfig, numinstances, replicagrouppartitionconfig, replica-group, consuming, completed]
level: advanced
status: docs-checked
description: "Pinot instanceAssignmentConfigMap: OFFLINE, CONSUMING and COMPLETED entries, tagPoolConfig, numInstances and replica-group settings."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/instance-assignment.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/rebalance/rebalance-servers/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance assignment config

By default every server of the cluster is assigned to each table with balanced segment assignment. Instance assignment narrows and structures that set via **InstanceAssignmentConfig**; each instance assignment strategy is tied to one segment assignment strategy. When it is configured explicitly, the result is stored in ZooKeeper under `PROPERTYSTORE/INSTANCE_PARTITIONS/`.
```
"instanceAssignmentConfigMap": {
  "CONSUMING": {
    "tagPoolConfig": { "tag": "DefaultTenant_REALTIME" },
    "replicaGroupPartitionConfig": {
      "replicaGroupBased": true, "numReplicaGroups": 2, "numInstancesPerReplicaGroup": 2 }
  },
  "COMPLETED": {
    "tagPoolConfig": { "tag": "DefaultTenant_OFFLINE" },
    "replicaGroupPartitionConfig": {
      "replicaGroupBased": true, "numReplicaGroups": 2, "numInstancesPerReplicaGroup": 4 }
  }
}
```
Entry types: `OFFLINE` (instances for an offline table), `CONSUMING` (consuming segments of a realtime table) and `COMPLETED` (completed segments). If `COMPLETED` is not configured, completed segments use the same assignment as consuming ones; if it is, they are moved to the `COMPLETED` instances periodically.

Parts:
- `tagPoolConfig.tag` selects the server pool. Servers carry tags in their Helix InstanceConfig, and the suffix `_OFFLINE` or `_REALTIME` says which table type they serve.
- `numInstances` limits how many servers a table uses (useful for tiny tables on a big cluster).
- `replicaGroupPartitionConfig` defines replica groups: `numReplicaGroups` with `numInstancesPerReplicaGroup`, and for partitioned replica groups `numPartitions` with `numInstancesPerPartition`.

Realtime LLC tables implicitly use partitioned replica-group assignment with `numPartitions` 1 and `numInstancesPerPartition` 1. To make `minimizeDataMovement` effective, set `partitionSelector` of the `CONSUMING` entry to `IMPLICIT_REALTIME_TABLE_PARTITION_SELECTOR`, which forces `numPartitions` to the real stream partition count.

Applying a changed assignment to existing segments requires a table rebalance with `reassignInstances=true` (see the rebalance skill); the assignment itself is only recomputed then.

## Checked

2026-11-09. Read the opening, default, tag-based, `numInstances`, replica-group, partitioned replica-group and LLC real-time sections of the Pinot docs page `instance-assignment.md`, and the `reassignInstances` text in the rebalance-servers page. Removed: the draft's `cold_OFFLINE` example with an empty COMPLETED replica config (replaced by the pattern the tuning docs show) and the "otherwise segments stay put" wording, now stated as the documented rebalance requirement. Not read: pool-based, fault-domain-aware and tier assignment sections in detail.
Method: documentation only; no commands were run.
