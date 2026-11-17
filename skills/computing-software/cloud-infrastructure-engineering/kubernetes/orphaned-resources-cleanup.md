---
id: computing-software.cloud-infrastructure-engineering.kubernetes.orphaned-resources-cleanup
name: orphaned-resources-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, garbage-collection, orphaned-resources, cascade-orphan, ownerreferences]
level: practitioner
status: docs-checked
description: "Find objects left without owners (orphaned ReplicaSets, pods, PVCs, Jobs) after cascade-orphan deletes or controller removal, and clean them up safely."
sources: ["https://kubernetes.io/docs/concepts/architecture/garbage-collection/", "https://kubernetes.io/docs/tasks/administer-cluster/use-cascading-deletion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding orphaned resources

Orphans come from `kubectl delete --cascade=orphan`, operators uninstalled before their
children, ownerReferences to UIDs that no longer exist (recreated owners), or manual creation.

## Pods and ReplicaSets with no owner
```bash
kubectl get pods -A -o json | jq -r '.items[] | select(.metadata.ownerReferences == null) | "\(.metadata.namespace)/\(.metadata.name)"'
kubectl get rs -A -o json | jq -r '.items[] | select(.metadata.ownerReferences == null) | "\(.metadata.namespace)/\(.metadata.name) replicas=\(.spec.replicas)"'
```
Standalone pods are sometimes legitimate (debug pods); check before deleting.

## Owner UID that no longer exists
The GC deletes dependents once all their owners are verified absent. Cross-namespace owner
references are disallowed: a namespaced owner must be in the dependent's namespace, otherwise the
reference is treated as absent. A cluster-scoped dependent that names a namespaced owner has an
unresolvable reference and is never garbage collected. Both cases raise a warning Event with
reason `OwnerRefInvalidNamespace`:
```bash
kubectl get events -A --field-selector reason=OwnerRefInvalidNamespace
```

## Old ReplicaSets with zero replicas
Not orphans but clutter: the Deployment's `.spec.revisionHistoryLimit` sets how many old
ReplicaSets are kept.
```bash
kubectl get rs -A --no-headers | awk '$3==0 && $4==0' | wc -l
```

## PVCs from deleted StatefulSets
```bash
kubectl get pvc -A -o json | jq -r '.items[] | select(.metadata.ownerReferences == null and (.metadata.labels.app // "") != "") | "\(.metadata.namespace)/\(.metadata.name)"'
kubectl get pods -A -o json | jq -r '.items[].spec.volumes[]?.persistentVolumeClaim.claimName' | sort -u > used.txt   # compare
```

## Clean up
- Re-adopt instead of deleting when the controller is recreated with the same selector.
- Delete only after confirming nothing references them; for PVCs, snapshot first.
- Tools: `kor` lists unused ConfigMaps, Secrets, PVCs, Services (no endpoints) and more, and
  `--ignore-owner-references` skips objects that have owners.

## Checked
2026-10-27 against Kubernetes docs (kubernetes/website main, v1.38 development tree; v1.37 is the
latest release: garbage collection, cascading deletion, Deployment) and the yonahd/kor README.
Confirmed: `--cascade=orphan|background|foreground`, the cross-namespace owner reference rules and
the `OwnerRefInvalidNamespace` event with its field-selector query, `.spec.revisionHistoryLimit`,
and kor's Service check and `--ignore-owner-references`. Corrected the description of invalid
owner references and removed an unchecked claim about mirror pod owners.
Method: documentation only; no commands were run.
