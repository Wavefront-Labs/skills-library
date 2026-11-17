---
id: computing-software.messaging-and-integration.strimzi.namespace-watch-options
name: namespace-watch-options
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [watch-namespaces, strimzi-namespace, watch-strategy]
level: practitioner
status: docs-checked
description: "Choose which namespaces the Cluster Operator watches."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Namespace watch options

**Goal:** pick a watch strategy that performs well.

The Cluster Operator can watch:

- a single selected namespace,
- a specific list of namespaces, or
- all namespaces in the cluster.

Watching a specific list of multiple namespaces has the biggest performance impact because of extra processing overhead. The recommended modes are a single namespace or all namespaces.

The setting is the `STRIMZI_NAMESPACE` environment variable on the operator Deployment: a comma-separated list. When it is not set, is empty, or is `*`, the operator operates in all namespaces. The deployment can use the downward API to set it to its own namespace:

```yaml
env:
  - name: STRIMZI_NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace
```

The Deployment file shipped in the release is `install/cluster-operator/060-Deployment-strimzi-cluster-operator.yaml`.

Isolate component types: each watched namespace should contain only one instance of a given component (one Kafka cluster, one Kafka Connect cluster). Multiple Connect or MirrorMaker 2 clusters managed by the Cluster Operator must each be in a separate namespace.

**Checklist**

1. Prefer one namespace or all namespaces.
2. Avoid long namespace lists.
3. Keep one Kafka cluster per watched namespace.

## Checked

2026-11-03. Confirmed in Namespace watch strategy and isolation: the three options, that watching a list has the biggest performance impact, recommended modes, STRIMZI_NAMESPACE semantics, and the one-component-per-namespace warning.

Method: documentation only; no commands were run.
