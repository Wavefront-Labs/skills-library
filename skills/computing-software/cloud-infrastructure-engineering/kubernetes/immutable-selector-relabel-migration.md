---
id: computing-software.cloud-infrastructure-engineering.kubernetes.immutable-selector-relabel-migration
name: immutable-selector-relabel-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, immutable-selector, label-selectors, deployments, statefulsets, migration]
level: practitioner
status: docs-checked
description: "Change a Deployment or StatefulSet selector, which is immutable, with an orphan-and-replace migration that keeps pods serving traffic throughout."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#label-selector-updates", "https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/", "https://github.com/kubernetes/kubernetes/blob/release-1.37/pkg/apis/apps/validation/validation.go", "https://kubernetes.io/docs/concepts/architecture/garbage-collection/#orphaned-dependents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing an immutable selector

`spec.selector` on apps/v1 Deployments, ReplicaSets, StatefulSets and DaemonSets cannot be
changed (`field is immutable`), including through `kubectl apply`, `kubectl edit` or
`helm upgrade`. Migration:

## Deployment
1. Add the new label to the pod template only (the selector still uses the old label):
   ```yaml
   template:
     metadata:
       labels: {app: web, app.kubernetes.io/name: web}   # new label added
   ```
   Roll out; every pod now has both labels.
2. Point Services, NetworkPolicies, PDBs and monitoring selectors at the new label.
3. Delete the Deployment but keep its pods and ReplicaSets:
   `kubectl delete deploy web --cascade=orphan`
4. Apply the Deployment with the new selector (`app.kubernetes.io/name: web`). The documentation
   describes this as a non-overlapping change: the old ReplicaSet is orphaned and a new one is
   created, while the orphaned ReplicaSet keeps its pods running meanwhile.
5. Once the new pods are Ready: `kubectl delete rs <old-rs>`.

## StatefulSet
`kubectl delete sts db --cascade=orphan`, then apply the new StatefulSet with the same name,
`serviceName` and `volumeClaimTemplates` (both also immutable) and the new selector, then
`kubectl rollout restart sts db` so every pod is recreated from the new template. Pods are named
`<statefulset>-<ordinal>`, and deleting a StatefulSet does not delete its volumes by default;
check `persistentVolumeClaimRetentionPolicy` before starting.

## Gotchas
- GitOps tools try to recreate the old object between steps; pause sync for this change.
- Helm: `helm upgrade` fails on the immutable field; delete with `--cascade=orphan`, then upgrade.

## Verify
`kubectl get pods -l app.kubernetes.io/name=web -o jsonpath='{..ownerReferences[0].name}'` shows
only the new ReplicaSet, and the Service endpoints never dropped to zero.

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37): Deployments "Label selector updates" (immutable after creation, cannot be changed with
patch, edit, apply or `helm upgrade`; `--cascade=orphan`; additions orphan the old ReplicaSet)
and StatefulSets (volumes not deleted with the StatefulSet, retention policy), plus
kubernetes/kubernetes release-1.37 apps validation (selector immutable for Deployment,
ReplicaSet, StatefulSet and DaemonSet; StatefulSet `serviceName` and `volumeClaimTemplates`
immutable) and apps/v1 types (pod naming). Removed the unconfirmed claim that a new StatefulSet
adopts orphaned pods by name.

Method: documentation only; no commands were run.
