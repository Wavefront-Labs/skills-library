---
id: computing-software.messaging-and-integration.strimzi.kafkatopic-naming
name: kafkatopic-naming
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafkatopic, topicname, strimzi-cluster-label]
level: practitioner
status: docs-checked
description: "Name KafkaTopic resources and map them to Kafka topic names."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KafkaTopic naming and ownership

**Goal:** make the Topic Operator see and manage your topics.

A `KafkaTopic` carries a name plus a label naming the Kafka cluster:

```yaml
apiVersion: kafka.strimzi.io/v1
kind: KafkaTopic
metadata:
  name: topic-name-1
  labels:
    strimzi.io/cluster: my-cluster
spec:
  topicName: topic-name-1
```

If the label does not match the cluster, the Topic Operator cannot see the resource and the topic is not created.

Kafka and Kubernetes have different naming rules. Guidelines: reflect the topic's nature, stay under 63 characters, use lower case and hyphens, avoid special characters, spaces and symbols.

`spec.topicName` is optional and defaults to `metadata.name`. Use it when the Kafka name is not a valid Kubernetes name:

```yaml
metadata:
  name: my-topic-1
spec:
  topicName: My.Topic.1
```

The topic name cannot be changed after creation. If several `KafkaTopic` resources point at one topic, the oldest manages it; the newer ones fail with a resource conflict error.

**Checklist**

1. Always set `strimzi.io/cluster`.
2. Use `spec.topicName` for upper case or dots.
3. Avoid two resources for one topic.

## Checked

2026-11-03. Confirmed in Topic naming conventions: strimzi.io/cluster label, guidelines (under 63 characters, lower case and hyphens), optional spec.topicName, and that only the oldest resource for a topic is reconciled. Removed the unconfirmed Ready=False status wording; the page says the newer resources fail with a resource conflict error.

Method: documentation only; no commands were run.
