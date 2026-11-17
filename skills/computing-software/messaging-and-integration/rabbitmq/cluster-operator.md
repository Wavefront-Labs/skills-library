---
id: computing-software.messaging-and-integration.rabbitmq.cluster-operator
name: cluster-operator
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, cluster-operator, rmq-kubernetes]
level: advanced
status: docs-checked
description: "Deploy RabbitMQ on Kubernetes with the Cluster Operator and a RabbitmqCluster resource."
sources:
  - https://www.rabbitmq.com/kubernetes/operator/using-operator
  - https://www.rabbitmq.com/kubernetes/operator/kubectl-plugin
  - https://www.rabbitmq.com/kubernetes/operator/install-operator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RabbitMQ Cluster Operator

**Goal:** Run clusters declaratively.

## Steps
1. Install the operator (`kubectl rabbitmq install-cluster-operator` with the plugin, or the manifest), then apply a `RabbitmqCluster` (`apiVersion: rabbitmq.com/v1beta1`) with `replicas: 3` and a persistence section.
2. Persistence: set `storageClassName` and `storage` (capacity); without a default StorageClass the pods will not schedule. Scheduling constraints go under `affinity`.
3. Admin credentials are stored in a generated Secret (named `<instance>-default-user`).
4. The `kubectl rabbitmq` plugin (installed with krew) provides commands such as `kubectl rabbitmq create INSTANCE`.

## Failure modes
- Setting `storage` to 0 deactivates persistence altogether, so data is lost on restart.
- `kubectl delete rabbitmqcluster INSTANCE` deletes the instance.

## Verify
- See "Verify the Instance is Running" in the using-operator guide.

## Checked

2026-11-02. Confirmed in the Cluster Operator guides: RabbitmqCluster v1beta1, replicas, storageClassName and storage, storage 0 behaviour, affinity field, default-user Secret, krew plugin, delete command. Removed: `kubectl get rabbitmqclusters` / AllReplicasReady and "anti-affinity" specifics (not in pages), "resource limits" wording.
Method: documentation only; no commands were run.
