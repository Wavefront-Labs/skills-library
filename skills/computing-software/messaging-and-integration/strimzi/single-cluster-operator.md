---
id: computing-software.messaging-and-integration.strimzi.single-cluster-operator
name: single-cluster-operator
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [cluster-operator-placement, avoid-conflicts, dedicated-namespace]
level: practitioner
status: docs-checked
description: "Plan one Cluster Operator per Kubernetes cluster and avoid CRD and version conflicts."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Planning your Cluster Operator deployment

**Goal:** avoid conflicts between Cluster Operators.

A single Cluster Operator can manage multiple Kafka clusters across namespaces. Running several instances, especially at different versions, risks:

- **Resource conflicts** over cluster-scoped resources such as CRDs and ClusterRoles. This happens even when the operators sit in separate namespaces.
- **Version incompatibility**, since releases may introduce changes that are not backward-compatible.

The recommended approach:

1. Run a single Cluster Operator per Kubernetes cluster.
2. Consider installing it in its own namespace, separate from the Kafka components it manages. This helps most when it watches multiple namespaces.
3. Keep Strimzi and the Kafka version it manages updated.

Inside each watched namespace, keep only one instance of a component type (for example one Kafka cluster). Otherwise you can get conflicting resource names, ambiguity in access management, topic and user name collisions, and unpredictable behaviour during upgrades or recovery.

```bash
kubectl get deployment strimzi-cluster-operator -n strimzi-operators
kubectl get crd | grep kafka.strimzi.io
```

**Checklist**

1. One operator per cluster, in a dedicated namespace.
2. One Kafka cluster per watched namespace.
3. Keep Strimzi and the Kafka version it manages regularly updated.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Planning your Cluster Operator deployment: avoiding conflicts, namespace isolation). The kubectl listing commands are generic and not from the page.
