---
id: computing-software.cloud-infrastructure-engineering.kubernetes.replicaset-direct-scaling-reverted
name: replicaset-direct-scaling-reverted
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, replicaset, replicaset-scaling, deployment, reconciliation, ownerreference]
level: practitioner
status: docs-checked
description: "Why scaling or editing a Deployment-owned ReplicaSet is reverted, how the owner chain decides, and the right object to change for each goal."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/", "https://kubernetes.io/docs/reference/using-api/server-side-apply/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling a ReplicaSet directly

## Symptom
```bash
kubectl scale rs web-7d9c4b --replicas=10
kubectl get rs web-7d9c4b      # back to the Deployment's count
```
The ReplicaSet has an ownerReference to Deployment `web` (`controller: true`). The Deployment
controller reconciles its ReplicaSets' `spec.replicas` to match the Deployment (and its rollout
state), overwriting your change. The Deployment documentation says not to manage ReplicaSets
owned by a Deployment.

## Find the owner
```bash
kubectl get rs web-7d9c4b -o jsonpath='{.metadata.ownerReferences[0].kind}/{.metadata.ownerReferences[0].name}{"\n"}'
```
Owner chain for pods: Pod -> ReplicaSet -> Deployment, possibly with an HPA or a GitOps manager
setting the Deployment above that.

## Change the right thing
| Goal | Change |
|---|---|
| more replicas | `kubectl scale deploy/web` (or the HPA min/max if an HPA targets it) |
| different image/env | Deployment pod template |
| keep one old pod for debugging | change its labels so it leaves the ReplicaSet (`kubectl label pod x app-`); the ReplicaSet replaces it |
| take over pods with a new controller | orphan: `kubectl delete deploy web --cascade=orphan` |

A ReplicaSet makes no effort to make existing Pods match a changed pod template, and for
Deployment-owned sets the Deployment controller owns the template anyway.

## Also reverted
- `kubectl scale deploy` when an HPA manages it: the HPA sets the count again at its next sync
  (`--horizontal-pod-autoscaler-sync-period`, default 15 seconds). Remove `spec.replicas` from
  manifests when an HPA owns it.
- Any field another controller or GitOps tool keeps applying.
Check `metadata.managedFields` to see which manager owns `spec.replicas`:
```bash
kubectl get deploy web --show-managed-fields -o yaml | grep -B3 -A3 'f:replicas'
```

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37): Deployments ("Do not manage ReplicaSets owned by a Deployment", `--cascade=orphan`),
ReplicaSet (isolating Pods by changing labels, no effort to make existing Pods match a new
template), HorizontalPodAutoscaler (sync period default 15 seconds, remove `spec.replicas`)
and Server-Side Apply (`--show-managed-fields`). Removed the "within a second" timing and the
unconfirmed Argo CD/Flux self-heal and Argo Rollouts specifics.

Method: documentation only; no commands were run.
