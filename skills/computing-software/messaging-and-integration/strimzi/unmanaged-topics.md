---
id: computing-software.messaging-and-integration.strimzi.unmanaged-topics
name: unmanaged-topics
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [strimzi-managed-false, unmanaged-topic, rename-kafkatopic]
level: advanced
status: docs-checked
description: "Stop the Topic Operator managing a topic without deleting the Kafka topic."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unmanaged topics

**Goal:** change or recreate a `KafkaTopic` resource while keeping the Kafka topic.

The Topic Operator manages only topics that have a `KafkaTopic`. If a resource exists, configuration changes made outside it are reverted. To pause management, annotate the resource:

```bash
kubectl annotate kafkatopic my-topic-1 strimzi.io/managed="false" --overwrite
kubectl get kafkatopic my-topic-1 -o yaml
```

The status should carry the condition `type: Unmanaged`, and `metadata.generation` must match `status.observedGeneration`. The resource is then no longer reconciled.

To rename the resource (`metadata.name` cannot be edited):

1. Annotate it as unmanaged.
2. Delete the original: `kubectl delete kafkatopic <name>`.
3. Recreate a `KafkaTopic` with a different `metadata.name` and `spec.topicName` pointing at the same Kafka topic.

To resume management of a resource you did not delete, set `strimzi.io/managed` back to `true`.

```yaml
metadata:
  annotations:
    strimzi.io/managed: "false"
```

**Checklist**

1. Verify the `Unmanaged` condition before deleting.
2. Reuse the same `spec.topicName` when recreating.
3. Reset `managed` to `true` to re-adopt.

## Checked

2026-11-03. Confirmed in the Managing KafkaTopic resources section: the strimzi.io/managed annotation, Unmanaged condition with observedGeneration, the rename procedure with kubectl delete kafkatopic and spec.topicName, and resuming management.

Method: documentation only; no commands were run.
