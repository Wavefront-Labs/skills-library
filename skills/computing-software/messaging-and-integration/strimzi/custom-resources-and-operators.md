---
id: computing-software.messaging-and-integration.strimzi.custom-resources-and-operators
name: custom-resources-and-operators
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [custom-resources, operators, reconciliation, crd]
level: intro
status: docs-checked
description: "Understand how Strimzi CRDs and operators reconcile Kafka components on Kubernetes."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Strimzi custom resources and operators

**Goal:** know what each Strimzi operator does and what happens when a resource is created, updated or deleted.

Strimzi extends Kubernetes with CRDs such as `Kafka`, `KafkaNodePool`, `KafkaTopic` and `KafkaUser`. CRDs need a one-time install, which typically needs cluster admin privileges. Custom resources share common configuration under `spec`. Access to manage them is limited to Strimzi administrators.

Operators watch the resources and reconcile with three operations:

- **Creation:** builds Kubernetes resources (Deployment, Pod, Service, ConfigMap) or configures items inside Kafka such as topics and users.
- **Update:** applies valid changes, which may trigger a rolling update. Rolling updates keep the cluster available but can disrupt clients.
- **Deletion:** Kubernetes garbage collection removes most dependents. For a Kafka cluster, PVCs are retained by default. For a Kafka topic, the topic is fully deleted from Kafka.

The Cluster Operator is required and must be deployed first; it handles the lifecycle of Kafka clusters. Drain Cleaner is deployed separately.

```bash
kubectl get crd | grep strimzi
kubectl get kafka,kafkanodepool,kafkatopic,kafkauser -n my-namespace
```

**Checklist**

1. Install the CRDs and Cluster Operator first.
2. Remember that deleting a `KafkaTopic` deletes the Kafka topic.
3. Restrict who can edit Strimzi resources to Strimzi administrators.

## Checked

2026-11-03. Confirmed in the Strimzi overview: CRD list, creation/update/deletion behaviour, PVCs retained for clusters, topics fully deleted, Cluster Operator deployed first, Drain Cleaner separate.

Method: documentation only; no commands were run.
