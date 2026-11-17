---
id: computing-software.cloud-infrastructure-engineering.kubernetes.recreate-deployment-strategy
name: recreate-deployment-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment, recreate-strategy, rolling-update, rwo-volumes, singleton, ckad]
level: practitioner
status: docs-checked
description: "Know when a Deployment needs strategy Recreate (RWO volumes, singletons, incompatible schema versions), what downtime it implies, and the safer alternatives."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#recreate-deployment", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recreate deployment strategy

```yaml
spec:
  replicas: 1
  strategy:
    type: Recreate        # a rollingUpdate block may not be specified with this type
```
With `.spec.strategy.type: Recreate` all existing Pods are killed before new ones are created.
When you upgrade a Deployment, Pods of the old revision are terminated immediately and
successful removal is awaited before any Pod of the new revision is created. Old and new
versions never run together; downtime lasts from termination through scheduling, startup and
readiness of the new Pods.

The guarantee covers upgrades only: if you manually delete a Pod, the ReplicaSet creates the
replacement immediately, even while the old Pod is still Terminating. For an "at most N Pods"
guarantee the Deployment docs point to a StatefulSet.

## When it is the right call
- A single-replica app with an exclusive volume (for example a ReadWriteOnce claim). The default
  RollingUpdate is `maxUnavailable: 25%` (rounded down, so 0 for one replica) and
  `maxSurge: 25%` (rounded up, so 1), meaning the new Pod is created before the old one is
  removed and the volume may still be in use by the old Pod. Recreate avoids that overlap.
- Software that must not run two instances at once (file locks, a single-writer scheduler) and
  has no leader election.
- Version N and N+1 cannot coexist (for example a destructive database migration); expand and
  contract migrations are the better fix.

## Alternatives to weigh
- RollingUpdate with explicit `maxSurge` and `maxUnavailable` (they cannot both be 0).
- A StatefulSet for stateful singletons.
- Leader election in the app so several replicas can roll safely.

## Gotchas
- Switching an existing Deployment from RollingUpdate to Recreate fails validation while the
  `rollingUpdate` block is still set; remove it in the same change, for example with a JSON
  patch that removes `/spec/strategy/rollingUpdate` and sets `/spec/strategy/type` to `Recreate`.
- A long `terminationGracePeriodSeconds` on the old Pods lengthens the outage, since removal of
  the old Pods is awaited.

## Verify
- [ ] During a rollout, `kubectl get pods -w` shows the old pod gone before the new one is created.
- [ ] Planned maintenance window covers measured outage time.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Deployments" (Recreate Deployment note,
Max Unavailable / Max Surge defaults and rounding) and the Deployment strategy validation in the
Kubernetes source (latest release v1.37.1). Confirmed: Recreate semantics and the manual-delete
caveat, StatefulSet pointer, rounding and 25% defaults, both-zero restriction, `rollingUpdate`
forbidden with Recreate. Removed unconfirmed claims (Multi-Attach error text, PDB behaviour,
the maxSurge 0 comparison).
Method: documentation only; no commands were run.
