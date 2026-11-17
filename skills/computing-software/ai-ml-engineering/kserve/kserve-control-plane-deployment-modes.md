---
id: computing-software.ai-ml-engineering.kserve.kserve-control-plane-deployment-modes
name: kserve-control-plane-deployment-modes
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [control-plane, deployment-modes, standard-deployment, knative-mode, gateway-api, kubernetes-ingress, hpa, keda, scale-to-zero, networkingkserveiogateway-api]
level: practitioner
status: docs-checked
description: "KServe control plane: InferenceService vs LLMInferenceService CRDs, Standard (Gateway API) vs Knative deployment modes, generated resources, and when to choose each."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/architecture/control-plane.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KServe control plane and deployment modes

Two CRDs: `InferenceService` (v1beta1; predictive models and standard GenAI) and `LLMInferenceService` (v1alpha1; prefix-aware routing, disaggregated serving, fine-grained GPU scheduling). The KServe Controller Manager watches them and reconciles Kubernetes resources; admission webhooks validate and mutate (defaults, sidecars). Other controllers: LocalModel (node-level model cache), InferenceGraph, TrainedModel.

## Standard Deployment mode (recommended for LLMs)
Generates Deployment, Service, HPA (optionally a KEDA ScaledObject) and a Gateway API `HTTPRoute` (or a Kubernetes Ingress). No cold start, no scale-to-zero, no request queuing. Networking is chosen by annotation:

```yaml
metadata:
  annotations:
    networking.kserve.io/gateway-api: "true"     # Gateway API (recommended)
    # networking.kserve.io/ingress-class: "nginx" # plain Ingress, limited
```

Plain Ingress cannot do percentage traffic splitting, path-based routing or the explain endpoint.

## Knative mode
KServe creates a Knative Service and an Istio VirtualService (Knative creates the Revision); pods carry a queue-proxy. Gives scale-to-zero (`minReplicas: 0`), activator queuing, revisions and native traffic splitting, at the cost of cold starts, queue-proxy overhead and Istio/Kourier dependency. In this mode `scaleTarget` is the concurrency target per pod.

## Choosing
Standard: production HA, predictable latency, streaming/long connections, multi-tenant isolation. Knative: bursty or unpredictable traffic, cost savings via scale-to-zero, dev/test.

## Checked

Checked 2026-11-08 against the KServe website page control-plane.md, read in full: the two CRDs and versions, generated resources per mode, the networking annotations, Ingress limitations, the Knative scaleTarget example, the mode comparison and the choosing guidance. Reworded the Knative generated-resources sentence to match the diagram (Knative controller creates the Revision).

Method: docs-only read of cited pages, 2026-11-08
