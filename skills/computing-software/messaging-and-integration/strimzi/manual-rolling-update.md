---
id: computing-software.messaging-and-integration.strimzi.manual-rolling-update
name: manual-rolling-update
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [manual-rolling-update, pod-annotation, strimzipodset]
level: advanced
status: docs-checked
description: "Trigger a rolling update of Kafka, Connect or MirrorMaker 2 with an annotation."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual rolling updates

**Goal:** restart pods in a controlled rolling update.

Annotate each pod to roll. When several pods are annotated, consecutive rolling updates run in the same reconciliation. If a rolling update is already replacing a pod, annotating it does not guarantee an extra restart.

```bash
kubectl annotate pod <cluster_name>-kafka-<index> strimzi.io/manual-rolling-update="true"
kubectl annotate pod <cluster_name>-connect-<index> strimzi.io/manual-rolling-update="true"
kubectl annotate pod <cluster_name>-mirrormaker2-<index> strimzi.io/manual-rolling-update="true"
```

Alternatively annotate the `StrimziPodSet` that manages the pods, named for example `my-cluster-kafka`, `my-connect-cluster-connect` or `my-mm2-cluster-mirrormaker2`. Warning: if you annotate a `StrimziPodSet` while the Cluster Operator is reconciling it, the annotation can be overwritten without triggering the update. To avoid the race, annotate the pods directly.

Prerequisites: a running Cluster Operator and the target cluster running. For Kafka to stay available, use replicated topics with a replication factor of at least 3.

**Checklist**

1. Annotate pods, not the pod set.
2. Ensure topics are replicated.
3. Wait for the next reconciliation (every two minutes by default); the annotation is removed when the pod's update completes.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Managing rolling updates: pod annotation and pod management annotation sections).
