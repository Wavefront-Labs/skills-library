---
id: computing-software.messaging-and-integration.strimzi.scale-brokers
name: scale-brokers
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [scale-brokers, kafkanodepool-replicas, auto-rebalance]
level: advanced
status: docs-checked
description: "Add or remove brokers by changing node pool replicas and trigger auto-rebalancing."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scaling brokers

**Goal:** scale a Kafka cluster safely.

Change `spec.replicas` in the `KafkaNodePool`:

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaNodePool
metadata:
  name: my-node-pool
  labels:
    strimzi.io/cluster: my-cluster
spec:
  replicas: 3
```

Scale carefully to avoid disruption or data loss. More brokers add resources and fault tolerance; fewer reduce consumption. The actual topic replication factor depends on available brokers and `default.replication.factor`.

**Auto-rebalancing:** a scaling event is a change to `spec.replicas` of an existing node pool. With auto-rebalancing, after adding brokers partitions are redistributed across the new brokers, and before removing brokers partitions are moved off them. On Kafka 4.3 or later, brokers scheduled for removal are automatically cordoned by setting `cordoned.log.dirs`, preventing new partition assignments while partitions move off.

Manual alternatives use Cruise Control `KafkaRebalance` in `add-brokers` or `remove-brokers` mode, or the partition reassignment tool.

**Checklist**

1. Scale one node pool at a time.
2. Rebalance partitions after adding brokers.
3. Move partitions off before removing brokers.

## Checked

2026-11-03. Confirmed in the scaling and auto-rebalancing sections: spec.replicas on KafkaNodePool, auto-rebalancing behaviour, cordoned.log.dirs on Kafka 4.3 or later, and add-brokers/remove-brokers KafkaRebalance modes.

Method: documentation only; no commands were run.
