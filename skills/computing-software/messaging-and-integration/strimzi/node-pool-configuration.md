---
id: computing-software.messaging-and-integration.strimzi.node-pool-configuration
name: node-pool-configuration
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [node-pools, kafkanodepool, pool-inheritance]
level: advanced
status: docs-checked
description: "Configure KafkaNodePool resources and understand inheritance from Kafka."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring node pools

**Goal:** define pools of nodes with the right roles, replicas and storage.

A node pool is a group of Kafka nodes in one cluster. The label `strimzi.io/cluster` names the `Kafka` resource the pool belongs to. A pool must define roles, number of replicas and storage. Optional properties: `resources`, `template` and `jvmOptions`.

Inheritance rules:

- A property not set in `KafkaNodePool` is inherited from `Kafka`.
- If set in both, the node pool value wins. For example `-Xmx: 1024m` in the pool beats `-Xms: 512m` in `Kafka.spec.kafka.jvmOptions` for those settings.
- `template` sections are **not merged**. If the pool defines only `podSet.metadata.labels` and `Kafka` defines `podSet.metadata.annotations` plus `pod.metadata.labels`, the pod labels from `Kafka` apply but the podSet annotations from `Kafka` are ignored because a podSet template already exists in the pool.

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaNodePool
metadata:
  name: pool-a
  labels:
    strimzi.io/cluster: my-cluster
spec:
  replicas: 3
  roles: [broker]
  storage:
    type: jbod
```

**Checklist**

1. Set roles, replicas and storage on every pool.
2. Repeat full `template` blocks rather than relying on merging.
3. Check the pool label matches the cluster name.

## Checked

2026-11-03. Confirmed in the node pool section: required roles/replicas/storage, inheritance from Kafka, pool values winning, and template sections not being merged.

Method: documentation only; no commands were run.
