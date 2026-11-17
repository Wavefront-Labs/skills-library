---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-resize-volumes
name: prometheus-operator-resize-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [volume-resize, statefulset-orphan, spec-paused, allowvolumeexpansion, pvc-expansion]
level: advanced
status: docs-checked
description: "Grow Prometheus storage when StatefulSets cannot expand volumes, by pausing the resource, patching PVCs and deleting the StatefulSet with orphan cascade."
sources: ["https://prometheus-operator.dev/docs/platform/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubernetes does not support volume expansion through StatefulSets. If you simply raise `spec.storage` on a custom resource, the operator deletes and recreates the StatefulSet, and the PVCs are not expanded. Do it by hand, with a StorageClass that allows expansion.

1. Check: `kubectl get storageclass -o custom-columns=NAME:.metadata.name,ALLOWVOLUMEEXPANSION:.allowVolumeExpansion`.
2. Pause the operator and update the request (example resource `example`, new size 10Gi):
```bash
kubectl patch prometheus/example --patch '{"spec": {"paused": true, "storage": {"volumeClaimTemplate": {"spec": {"resources": {"requests": {"storage":"10Gi"}}}}}}}' --type merge
```
3. Patch every PVC:
```bash
for p in $(kubectl get pvc -l operator.prometheus.io/name=example -o jsonpath='{range .items[*]}{.metadata.name} {end}'); do
  kubectl patch pvc/${p} --patch '{"spec": {"resources": {"requests": {"storage":"10Gi"}}}}'
done
```
4. Delete the StatefulSet without touching pods: `kubectl delete statefulset -l operator.prometheus.io/name=example --cascade=orphan`.
5. Unpause: `kubectl patch prometheus/example --patch '{"spec": {"paused": false}}' --type merge`.

The operator recreates the StatefulSet immediately; with the orphan strategy there is no service disruption and the mounted volumes show the new size.

## Checked

2026-11-08. Read the storage page in full. Commands match the docs; no changes needed.

Method: documentation only; no commands were run.
