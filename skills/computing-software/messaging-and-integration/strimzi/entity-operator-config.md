---
id: computing-software.messaging-and-integration.strimzi.entity-operator-config
name: entity-operator-config
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [entity-operator, topicoperator-userop, entityoperator-spec]
level: advanced
status: docs-checked
description: "Configure the Entity Operator that runs the Topic and User Operators."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuring the Entity Operator

**Goal:** deploy the Topic Operator and User Operator with a cluster.

Configure `Kafka.spec.entityOperator`. It contains the Topic Operator and User Operator, and supports `topicOperator`, `userOperator` and `template` (labels, annotations, affinity, tolerations of the pod).

```yaml
spec:
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

Rules:

- If `topicOperator` is missing, the Entity Operator is deployed without the Topic Operator; same for `userOperator`.
- An empty object `{}` uses all default values.
- If both are missing, the Entity Operator is **not deployed**.
- Each operator watches a single namespace, by default the Kafka cluster's namespace.

Topic Operator properties include `watchedNamespace`, `reconciliationIntervalMs` (default 120000), `image`, `resources` and `logging`:

```yaml
topicOperator:
  watchedNamespace: my-topic-namespace
  reconciliationIntervalMs: 60000
```

Watching another namespace requires enabling `STRIMZI_ENTITY_OPERATOR_WATCHED_NAMESPACE_ENABLED` to `true` in the Cluster Operator.

**Checklist**

1. Include both operators if you manage topics and users declaratively.
2. Set resource requests on each.
3. Enable the watched-namespace variable before changing `watchedNamespace`.

## Checked

2026-11-03. Confirmed in the Entity Operator configuration section: topicOperator/userOperator/template, empty-object defaults, the watchedNamespace and reconciliationIntervalMs (120000) properties, and the STRIMZI_ENTITY_OPERATOR_WATCHED_NAMESPACE_ENABLED requirement.

Method: documentation only; no commands were run.
