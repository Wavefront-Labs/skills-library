---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volume-populators-datasourceref
name: volume-populators-datasourceref
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-snapshots, volume-populator, datasourceref, csi, pvc]
level: practitioner
status: docs-checked
description: "Pre-fill new PVCs from snapshots, other PVCs or custom populator resources using dataSourceRef, and know how it differs from dataSource."
sources: ["https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#volume-populators-and-data-sources", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/", "https://github.com/kubernetes-csi/lib-volume-populator", "https://github.com/kubernetes-csi/volume-data-source-validator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume populators and dataSourceRef

## dataSource vs dataSourceRef
| | dataSource | dataSourceRef |
|---|---|---|
| Kinds | PVC, VolumeSnapshot | any object in the same namespace except core objects other than PVCs, including custom resources |
| Invalid value | ignored, as if the field was blank | never ignored; causes an error |
| Cross-namespace | no | alpha since 1.26 with `CrossNamespaceVolumeDataSource` plus a ReferenceGrant (Gateway API) |
If only one is set the API server gives both the same value; different values are a validation error and neither can change after creation. Prefer `dataSourceRef` when the feature gate is enabled: `AnyVolumeDataSource` is stable since 1.33 per the feature-gate page (beta from 1.24 to 1.32, where it needed enabling on kube-apiserver and kube-controller-manager).

## Clone or restore
```yaml
spec:
  dataSourceRef: {kind: PersistentVolumeClaim, name: golden-image}
  # or {apiGroup: snapshot.storage.k8s.io, kind: VolumeSnapshot, name: nightly}
```

## Custom populator
A populator is a controller that watches for PVCs that reference a custom resource in `dataSourceRef` and
fills the new volume from it. Registering the kind with the optional volume-data-source-validator (alpha)
uses a `VolumePopulator` object:
```yaml
apiVersion: populator.storage.k8s.io/v1beta1
kind: VolumePopulator
metadata: {name: hello-populator}
sourceKind: {group: hello.example.com, kind: Hello}
```
Install the volume-data-source-validator so PVCs pointing at kinds with no registered populator get a
warning event. External populators are responsible for reporting events about volume creation.

## Verify
```bash
kubectl describe pvc <name>        # events from the populator or validator
```
The PVC binds and contains the expected data; an invalid `dataSourceRef` produces an error instead of
silently creating an empty volume.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: dataSource vs dataSourceRef differences and syncing, cross-namespace alpha since 1.26 with ReferenceGrant, the validator's role (alpha, warning events), AnyVolumeDataSource gate stages (feature-gate page: stable from 1.33), and the VolumePopulator v1beta1 shape (top-level sourceKind of group/kind, no spec) from the validator repo's types and examples. Corrected the VolumePopulator example, which wrongly had a `spec.dataSourceRef`. Removed the unconfirmed temporary-PVC rebinding description and the KubeVirt/backup-tool examples.

Method: documentation only; no commands were run.
