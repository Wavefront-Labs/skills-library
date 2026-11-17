---
id: computing-software.messaging-and-integration.strimzi.deploy-kafka-connect
name: deploy-kafka-connect
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafkaconnect, connect-workers, distributed-mode]
level: practitioner
status: docs-checked
description: "Deploy a Kafka Connect cluster with the KafkaConnect resource."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying Kafka Connect

**Goal:** run Kafka Connect workers managed by the Cluster Operator.

Kafka Connect streams data between Kafka and external systems using connector plugins. In Strimzi it is deployed in **distributed mode**; standalone mode is not supported. The Cluster Operator manages clusters declared by `KafkaConnect` and connectors declared by `KafkaConnector`.

The deployment is a configurable number of workers that distribute connector tasks. The example file is `examples/connect/kafka-connect.yaml`.

Prerequisites: Cluster Operator deployed and a Kafka cluster running.

```bash
kubectl apply -f examples/connect/kafka-connect.yaml
kubectl get pods -n my-namespace
```

Warning from the docs: when deploying multiple Connect clusters managed by the Cluster Operator, put each in a separate namespace. Same-namespace deployments can cause naming conflicts and resource collisions.

After the cluster is running, add connector plugins and connector instances. Plugins can be added by building a new image automatically, mounting plugins as Kubernetes Image volumes, or building a custom image from the base Connect image.

**Checklist**

1. One Connect cluster per namespace.
2. Check the Kafka cluster is running first.
3. Add plugins, then create connectors.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Deploying Kafka Connect, 7.3 and 7.3.1; Adding Kafka Connect connectors).
