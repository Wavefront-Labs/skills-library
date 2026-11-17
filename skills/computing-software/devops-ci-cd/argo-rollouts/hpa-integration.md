---
id: computing-software.devops-ci-cd.argo-rollouts.hpa-integration
name: hpa-integration
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [hpa, autoscaling, horizontal-pod-autoscaler, scale-subresource, replicas, rollout, argo-rollouts]
level: practitioner
status: docs-checked
description: "Let a Kubernetes HorizontalPodAutoscaler scale a Rollout through its /scale subresource."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/hpa-support/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Argo Rollouts works with the standard HPA via `autoscaling/v2beta` or later and the stable `autoscaling/v2` (Kubernetes 1.23+). Since v0.3.0 the Rollout exposes the `/scale` subresource just like a Deployment, so the HPA can discover it.

The division of labour: the HPA decides the total desired replica count from CPU, memory or custom metrics and writes it to the Rollout's `spec.replicas`. It does not manage ReplicaSets directly. Argo Rollouts then carries out the deployment, allocating pods across stable, canary or preview ReplicaSets according to the strategy.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rollout-hpa
spec:
  scaleTargetRef:
    apiVersion: argoproj.io/v1alpha1
    kind: Rollout
    name: rollout-hpa-example
  minReplicas: 3
  maxReplicas: 10
```

Use the same pattern for blue-green (stable and preview Services) or canary.

Related details from the specification: while a rollout is manually `paused`, HPA scaling still occurs. For fast promotion under varying load, the `replicaProgressThreshold` canary step sets how many replicas must be ready (Percent or Pod) instead of 100%.

Verify: the HPA's `scaleTargetRef` names the Rollout, and the Rollout's `spec.replicas` changes as the HPA scales it under load.

## Checked

2026-11-08. Confirmed against the Argo Rollouts HPA support page (read in full): autoscaling/v2beta or higher and autoscaling/v2, /scale subresource since v0.3.0, HPA writes spec.replicas. The manual pause and replicaProgressThreshold notes are confirmed against the specification page (the relevant spec comments were read; the page was searched for HPA, paused and replicaProgressThreshold, not read in full).

Removed or corrected: removed the VPA support remark and the kubectl verify commands (not on the cited pages).

Method: documentation only; no commands were run.
