---
id: computing-software.messaging-and-integration.strimzi.kraft-node-roles
name: kraft-node-roles
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kraft, controller-nodes, broker-nodes, dual-role]
level: practitioner
status: docs-checked
description: "Assign controller, broker or dual roles to node pools in a KRaft-mode Kafka cluster."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KRaft mode and node roles

**Goal:** deploy Kafka without ZooKeeper using `Kafka` plus `KafkaNodePool` resources.

KRaft (Kafka Raft metadata) mode replaces ZooKeeper for cluster management. To deploy a cluster in KRaft mode you must use `Kafka` and `KafkaNodePool` custom resources. Node pools assign each node a role:

- **Controller** nodes run the control plane and manage metadata with a Raft-based consensus protocol.
- **Broker** nodes run the data plane: they receive and store data in topic partitions.
- **Dual-role** nodes do both.

Controllers keep a metadata log, a single-partition topic named `__cluster_metadata`, on every node. The active (lead) controller manages updates to the log and follower controllers replicate them. The log records brokers, replicas, topics and partitions, including in-sync replica state and partition leadership. Broker nodes act as observers and store the log passively.

Roles are set in the pool:

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaNodePool
metadata:
  name: dual-role
  labels:
    strimzi.io/cluster: my-cluster
spec:
  replicas: 3
  roles: [controller, broker]
```

Example files include `kafka-with-dual-role-nodes.yaml` and `kafka-persistent.yaml` (separate controller and broker pools).

**Checklist**

1. Label every pool with `strimzi.io/cluster`.
2. Set `spec.roles` explicitly.
3. Use the example files as a starting point.

## Checked

2026-11-03. Confirmed in the KRaft section: Kafka plus KafkaNodePool required, controller/broker/dual roles, the __cluster_metadata log and observer behaviour.

Method: documentation only; no commands were run.
