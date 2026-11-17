---
id: computing-software.messaging-and-integration.strimzi.deploy-kafka-example-files
name: deploy-kafka-example-files
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafka-deployment, example-files, node-pool-examples]
level: practitioner
status: docs-checked
description: "Deploy a Kafka cluster and node pools from the provided example files."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying a Kafka cluster from examples

**Goal:** create a Kafka resource and KafkaNodePool resources that the Cluster Operator manages.

To manage a cluster with the Cluster Operator it must be deployed as a `Kafka` resource. A cluster not deployed this way, such as one outside Kubernetes, cannot be managed by it, although the Topic Operator and User Operator can be deployed standalone against it.

One `Kafka` resource deploys the Kafka cluster, Topic Operator and User Operator. Node pools are groups of nodes sharing configuration; anything not set in a pool is inherited from the `Kafka` resource.

Example files in the release:

- `kafka/kafka-with-dual-role-nodes.yaml`: one pool with broker and controller roles.
- `kafka/kafka-persistent.yaml`: persistent cluster with a controller pool and a broker pool.
- `kafka/kafka-ephemeral.yaml`: ephemeral version of the same layout.
- `kafka/kafka-single-node.yaml`: a single node.
- `kafka/kafka-jbod.yaml`: multiple volumes per broker.

```bash
kubectl apply -f examples/kafka/kafka-with-dual-role-nodes.yaml
kubectl get pods -n my-namespace
```

**Checklist**

1. Pick the example matching your storage needs.
2. Do not use ephemeral or single-node examples for production data.
3. Wait for pods to reach Running before creating topics.

## Checked

2026-11-03. Confirmed in Deploying a Kafka cluster: the Kafka resource requirement, standalone Topic/User Operator note, and the example files listed.

Method: documentation only; no commands were run.
