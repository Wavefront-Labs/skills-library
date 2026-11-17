---
id: computing-software.messaging-and-integration.rabbitmq.topology-operator
name: topology-operator
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, topology-operator]
level: advanced
status: docs-checked
description: "Manage queues, exchanges, bindings, policies and users as Kubernetes resources."
sources:
  - https://www.rabbitmq.com/kubernetes/operator/using-topology-operator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Messaging Topology Operator

**Goal:** GitOps for broker topology.

## Steps
1. Install the Messaging Topology Operator; declare `Queue`, `Policy` and other topology custom resources (`apiVersion: rabbitmq.com/v1beta1`) that reference a `RabbitmqCluster`.
2. Set `deletionPolicy` (`delete` or `retain`, per the "Delete a Resource" section of the guide) to control what happens in RabbitMQ when the Kubernetes resource is deleted.
3. Keep client declarations consistent with the custom resources.

## Failure modes
- Drift if apps also declare conflicting queue arguments.

## Verify
- Check the custom resource status in Kubernetes, then confirm in the management UI or with `rabbitmqctl list_queues`.

## Checked

2026-11-02. Confirmed in the using-topology-operator guide: `rabbitmq.com/v1beta1` Queue and Policy resources, deletionPolicy values delete and retain. Removed: `kubectl get queues` and the full kind list (Exchange, Binding, User not seen in the page text I read), and the Install step's operator-specific wording.
Method: documentation only; no commands were run.
