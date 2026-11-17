---
id: computing-software.devops-ci-cd.argo-rollouts.traffic-management-overview
name: traffic-management-overview
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [traffic-management, canaryservice, stableservice, trafficrouting, service-mesh, ingress, argo-rollouts]
level: practitioner
status: docs-checked
description: "Understand how Argo Rollouts drives traffic routers through canary and stable Services and which providers are supported."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/
  - https://argo-rollouts.readthedocs.io/en/stable/FAQ/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Traffic management means controlling the data plane with routing rules: raw percentages, header-based routing, or mirroring (copy traffic to the new version and ignore its responses). Core Kubernetes only offers Service load balancing, so Argo Rollouts manipulates a service mesh or ingress controller.

Supported providers: AWS ALB Ingress Controller, Ambassador Edge Stack, Apache APISIX, Google Cloud, Gateway API (plugin), HAProxy Ingress, Istio, Kong Ingress, NGINX Ingress Controller, Service Mesh Interface (SMI), Traefik Proxy, and multiple providers at once. No new traffic managers are accepted in the core controller; write a plugin instead (see traffic-router-plugins).

Whatever the provider, the Rollout must name a canary Service and a stable Service:

```yaml
strategy:
  canary:
    canaryService: canary-service
    stableService: stable-service
    trafficRouting: {}
```

The controller edits the Services' selectors to point at the canary and stable ReplicaSets, and the router uses them for weighting.

With traffic routing the stable ReplicaSet stays fully scaled during the update, because the controller assumes the application can take 100% of traffic if fully scaled and leaves further scaling to the HPA. Canary pods are scaled to match the weight. See canary-dynamic-stable-scale to change this.

The controller marks Services and Ingresses it modifies with the annotation `argo-rollouts.argoproj.io/managed-by-rollouts`, used to revert them when the Rollout is deleted.

Verify: the canary and stable Services' selectors point at the canary and stable ReplicaSets as the rollout progresses.

## Checked

2026-11-08. Confirmed against the Argo Rollouts traffic management page (read in full): techniques, provider list, plugin-only rule, canaryService and stableService, stable ReplicaSet kept fully scaled, and the managed-by-rollouts annotation from the FAQ (read in full).

Removed or corrected: replaced the unsourced kubectl get svc verify command.

Method: documentation only; no commands were run.
