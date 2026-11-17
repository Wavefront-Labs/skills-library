---
id: computing-software.devops-ci-cd.argo-rollouts.canary-dynamic-canary-scale
name: canary-dynamic-canary-scale
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [canary, setcanaryscale, matchtrafficweight, traffic-routing, shadowing, argo-rollouts]
level: advanced
status: docs-checked
description: "Decouple canary pod count from traffic weight with setCanaryScale when a traffic router is in use."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/canary/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default, with a traffic router, the canary is scaled to match the step's traffic weight: at 25% with four replicas, one canary pod. `setCanaryScale` breaks that link. It works only with a traffic router, because basic canary must control scale to approximate weight.

Use cases from the docs: scale the canary up for testing while `setWeight: 0` keeps it from public traffic; scale minimally and use header-based routing to reach it; scale to 100% to support traffic shadowing.

```yaml
steps:
  - setCanaryScale:
      replicas: 3        # explicit count
  - setCanaryScale:
      weight: 25         # percent of spec.replicas
  - setCanaryScale:
      matchTrafficWeight: true   # restore default
```

Danger: after an explicit `setCanaryScale`, `setWeight` no longer drives scale, so traffic can be badly unbalanced. This sequence on 10 replicas sends 90% of traffic to one pod:

```yaml
- setCanaryScale: { weight: 10 }
- setWeight: 90
- pause: {}
```

Reset with `matchTrafficWeight: true` so later `setWeight` steps create matching replicas again.

The spec also documents `replicaProgressThreshold` (type `Percent` or `Pod`, value) as a step: it sets how many replicas must be available before promotion, useful with an HPA. The checked value is available replicas divided by desired replicas for the step; default is 100%.

Verify the pod count with `kubectl argo rollouts get rollout NAME`.

## Checked
2026-11-08. Confirmed against the Argo Rollouts Canary page and Rollout Specification page: default scale matching traffic weight, the three use cases, `setCanaryScale` with `replicas`, `weight` and `matchTrafficWeight`, the traffic-router-only restriction, the 90 percent of traffic to 10 percent of pods example, and `replicaProgressThreshold` with its type, default and formula. Nothing removed.
Method: documentation only; no commands were run.
