---
id: computing-software.messaging-and-integration.strimzi.listener-types
name: listener-types
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafka-listeners, generickafkalistener, listener-type]
level: advanced
status: docs-checked
description: "Choose between internal and external listener types."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kafka listener types

**Goal:** expose Kafka to the right clients.

Listeners are configured with `GenericKafkaListener` entries in `Kafka.spec.kafka.listeners`. Services, routes, load balancers and ingresses are created according to the type.

**Internal** (inside the Kubernetes cluster):

- `internal`: connect within the same cluster, via the headless service and broker pod DNS names. By default they do not use the service DNS domain (`.cluster.local`); the `useServiceDnsDomain` property changes this.
- `cluster-ip`: per-broker ClusterIP services. Consider it when the headless service is not feasible or for Ingress controllers or Gateway API integration.

**External** (outside the cluster):

- `nodeport`: ports on Kubernetes nodes
- `loadbalancer`: loadbalancer services
- `tlsroute`: Kubernetes Gateway API v1 `TLSRoute` resources
- `ingress`: Kubernetes Ingress (Kubernetes only)
- `route`: OpenShift routes (OpenShift only)

```yaml
listeners:
  - name: plain
    port: 9092
    type: internal
    tls: false
  - name: tls
    port: 9093
    type: internal
    tls: true
```

**Checklist**

1. Use unique listener names and ports.
2. Pick an external type matching your platform.
3. Add `authentication` per listener.

## Checked

2026-11-03. Confirmed in Configuring listeners: internal and cluster-ip behaviour, useServiceDnsDomain, and the external types nodeport, loadbalancer, tlsroute, ingress and route with their platform limits.

Method: documentation only; no commands were run.
