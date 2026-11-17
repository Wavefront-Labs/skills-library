---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rollout-change-cause-annotations
name: rollout-change-cause-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment, change-cause, rollout-history, rollout-undo]
level: practitioner
status: docs-checked
description: "Record why each Deployment revision exists with the kubernetes.io/change-cause annotation, now that --record is deprecated, and use it to pick rollback targets."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#checking-rollout-history-of-a-deployment", "https://kubernetes.io/docs/reference/labels-annotations-taints/#change-cause"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change-cause annotations

`kubectl rollout history` shows a CHANGE-CAUSE column. CHANGE-CAUSE is copied from the
Deployment annotation `kubernetes.io/change-cause` to its revisions upon creation. The old
`--record` flag that filled it automatically is deprecated and will be removed in a future
release, so set the annotation explicitly.

## Set it with each change
```bash
kubectl set image deployment/web web=web:1.5.0
kubectl annotate deployment/web kubernetes.io/change-cause="1.5.0: new checkout flow (CHG-1234)" --overwrite
```
The docs list three ways to specify it: `kubectl annotate` on the Deployment, editing the
manifest, or tooling that sets the annotation automatically. In a manifest the annotation
belongs on the Deployment's own `metadata`:
```yaml
metadata:
  annotations:
    kubernetes.io/change-cause: "deploy ${GIT_SHA} by ${CI_PIPELINE_ID}"
```
Because the value is copied when a revision is created, set it in the same apply as the
template change.

## Use it
```bash
kubectl rollout history deployment/web
# REVISION  CHANGE-CAUSE
kubectl rollout history deployment/web --revision=3      # details of revision 3
kubectl rollout undo deployment/web --to-revision=3
```

## Gotchas
- A rollout is triggered if and only if `.spec.template` changes, and a revision is created when
  a rollout is triggered; changing only the annotation creates no revision.
- Each rollback updates the revision of the Deployment, so check history after an undo and
  annotate it with the reason for the rollback.
- Rollback targets are limited by `.spec.revisionHistoryLimit` (default 10 old ReplicaSets);
  once an old ReplicaSet is deleted you cannot roll back to that revision.
- In GitOps setups the Git log is the real history; the annotation helps on-call engineers at the
  kubectl prompt.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Deployments" (rollout history, rolling back,
revision history limit) and "Well-Known Labels, Annotations and Taints" (change-cause) (latest
release v1.37.1). Confirmed: copy-on-revision-creation behaviour, `--record` deprecation, the
three ways to set it, `--revision` and `--to-revision`, template-only rollout trigger, default
history limit of 10. Removed unconfirmed claims (annotation copied onto the current ReplicaSet
when annotating after a rollout, rollback retaining the old change-cause) and the sample history
rows.
Method: documentation only; no commands were run.
