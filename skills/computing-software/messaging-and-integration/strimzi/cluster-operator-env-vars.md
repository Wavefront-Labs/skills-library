---
id: computing-software.messaging-and-integration.strimzi.cluster-operator-env-vars
name: cluster-operator-env-vars
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [cluster-operator-config, strimzi-env-vars, reconciliation-interval]
level: advanced
status: docs-checked
description: "Tune the Cluster Operator through its environment variables and defaults."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cluster Operator environment variables

**Goal:** set the operator's behaviour on its Deployment.

Configure the Cluster Operator through environment variables in `install/cluster-operator/060-Deployment-strimzi-cluster-operator.yaml`.

| Variable | Default / meaning |
|---|---|
| `STRIMZI_NAMESPACE` | Namespaces to operate in; unset, empty or `*` means all |
| `STRIMZI_FULL_RECONCILIATION_INTERVAL_MS` | 120000 ms between periodic reconciliations |
| `STRIMZI_OPERATION_TIMEOUT_MS` | 300000 ms timeout for internal operations |
| `STRIMZI_OPERATIONS_THREAD_POOL_SIZE` | 10 worker threads |
| `STRIMZI_FEATURE_GATES` | `+Gate` / `-Gate` list |
| `STRIMZI_CUSTOM_RESOURCE_SELECTOR` | Label selector; only matching resources are seen |

The docs advise increasing `STRIMZI_OPERATION_TIMEOUT_MS` where Kubernetes operations are slow, for example from long image pulls.

`STRIMZI_CUSTOM_RESOURCE_SELECTOR` applies to `Kafka`, `KafkaConnect`, `KafkaBridge` and `KafkaMirrorMaker2`. `KafkaRebalance` and `KafkaConnector` are operated only when their Kafka or Connect cluster carries the matching labels.

```yaml
env:
  - name: STRIMZI_FULL_RECONCILIATION_INTERVAL_MS
    value: "120000"
```

**Checklist**

1. Edit the Deployment, then confirm the pod restarted.
2. Raise the operation timeout on slow clusters.
3. Use the selector to split ownership between operators carefully.

## Checked

2026-11-03. Confirmed in the Cluster Operator configuration section: the 060 Deployment file name, STRIMZI_NAMESPACE semantics, 120000 ms and 300000 ms defaults, thread pool default 10, the timeout advice (slow image pulls), STRIMZI_CUSTOM_RESOURCE_SELECTOR scope, and the +/- STRIMZI_FEATURE_GATES syntax.

Method: documentation only; no commands were run.
