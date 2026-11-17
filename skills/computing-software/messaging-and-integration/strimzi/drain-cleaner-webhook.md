---
id: computing-software.messaging-and-integration.strimzi.drain-cleaner-webhook
name: drain-cleaner-webhook
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [drain-cleaner, validatingwebhook, pod-eviction]
level: advanced
status: docs-checked
description: "Understand how Strimzi Drain Cleaner intercepts evictions."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drain Cleaner webhook

**Goal:** know what the Drain Cleaner registers and what it does.

Drain Cleaner is deployed separately. Its deployment includes a `ValidatingWebhookConfiguration`:

```yaml
webhooks:
  - name: strimzi-drain-cleaner.strimzi.io
    rules:
      - apiGroups: [""]
        apiVersions: ["v1"]
        operations: ["CREATE"]
        resources: ["pods/eviction"]
        scope: "Namespaced"
    clientConfig:
      service:
        namespace: "strimzi-drain-cleaner"
        name: "strimzi-drain-cleaner"
        path: /drainer
        port: 443
```

Only `CREATE` operations on `pods/eviction` are evaluated. The webhook listens on `/drainer` over TLS; `caBundle` provides the CA. Unless you use your own certificates, no manual configuration is needed.

Two modes:

- **Default:** denies the eviction request and instead has the Cluster Operator move the pod; works better with cluster autoscaling tools and needs no specific PodDisruptionBudget.
- **Legacy:** allows the eviction while asking the Cluster Operator to move the pod; needs a PodDisruptionBudget with `maxUnavailable: 0`.

**Checklist**

1. Deploy with a highly available Kafka cluster.
2. Choose default or legacy mode deliberately.
3. Renew its TLS certificates when needed.

## Checked

2026-11-03. Confirmed in the Drain Cleaner section: the ValidatingWebhookConfiguration rules, /drainer path, default vs legacy mode, and maxUnavailable 0 PodDisruptionBudget for legacy mode.

Method: documentation only; no commands were run.
