---
id: computing-software.messaging-and-integration.strimzi.kafkaconnector-resources
name: kafkaconnector-resources
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafkaconnector, use-connector-resources, tasksmax]
level: advanced
status: docs-checked
description: "Manage connector instances declaratively with KafkaConnector resources."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KafkaConnector resources

**Goal:** create, reconfigure and delete connectors through Kubernetes.

Enable the annotation on the `KafkaConnect` resource:

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaConnect
metadata:
  name: my-connect-cluster
  annotations:
    strimzi.io/use-connector-resources: "true"
```

This switches connector management from the Kafka Connect REST API to custom resources managed by the Cluster Operator; you must then define connectors with `KafkaConnector`. To use the REST API instead, remove the annotation.

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaConnector
metadata:
  name: my-source-connector
  labels:
    strimzi.io/cluster: my-connect-cluster
spec:
  class: org.apache.kafka.connect.file.FileStreamSourceConnector
  tasksMax: 2
  autoRestart:
    enabled: true
  config:
    file: "/opt/kafka/LICENSE"
    topic: my-topic
```

`metadata.name` is the connector name; the label `strimzi.io/cluster` names the Connect cluster. `tasksMax` sets the maximum number of tasks, so a source connector with `tasksMax: 2` might split the import into two tasks. The Kafka cluster need not be managed by Strimzi or run in Kubernetes.

**Checklist**

1. Set the annotation first.
2. Label each connector with the Connect cluster name.
3. Use configuration providers for credentials, as the docs recommend.

## Checked

2026-11-03. Confirmed in the Kafka Connect section: the use-connector-resources annotation, KafkaConnector fields, the strimzi.io/cluster label, and that the Kafka cluster need not be managed by Strimzi or run on Kubernetes.

Method: documentation only; no commands were run.
