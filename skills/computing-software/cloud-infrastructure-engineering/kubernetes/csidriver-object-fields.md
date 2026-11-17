---
id: computing-software.cloud-infrastructure-engineering.kubernetes.csidriver-object-fields
name: csidriver-object-fields
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csi, csidriver-object, attachrequired, fsgroup, csi-driver]
level: practitioner
status: docs-checked
description: "Configure the CSIDriver object (attachRequired, podInfoOnMount, fsGroupPolicy, volumeLifecycleModes, tokenRequests, storageCapacity) and what each changes."
sources: ["https://kubernetes-csi.github.io/docs/csi-driver-object.html", "https://kubernetes.io/docs/concepts/storage/volumes/#csi", "https://github.com/kubernetes/api/blob/master/storage/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSIDriver object

Cluster-scoped, named after the driver (`ebs.csi.aws.com`), usually installed by the driver's
Helm chart. It tells Kubernetes how to treat the driver.

```yaml
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata: {name: example.csi.vendor.io}
spec:
  attachRequired: true
  podInfoOnMount: false
  fsGroupPolicy: File
  volumeLifecycleModes: [Persistent]
  storageCapacity: false
  requiresRepublish: false
  seLinuxMount: false
  tokenRequests:
  - audience: "vault"
    expirationSeconds: 3600
```

## Fields
| Field | Effect |
|---|---|
| `attachRequired` | true (the default, also when no CSIDriver object exists): Kubernetes calls attach and waits for it before mounting. false: attach is skipped (for drivers that do not implement `ControllerPublishVolume`) |
| `podInfoOnMount` | true: kubelet passes pod name, namespace, UID and service account name in `volume_context` of `NodePublishVolume`; false or unset: not passed |
| `fsGroupPolicy` | `ReadWriteOnceWithFSType` (default: only if `fsType` is defined and the PV's accessModes contain `ReadWriteOnce`), `File` (fsGroup may be applied regardless of fstype or access mode), `None` (volume mounted unmodified). GA since Kubernetes 1.23 |
| `volumeLifecycleModes` | `Persistent` (default, normal PVC/PV), `Ephemeral` (inline CSI ephemeral volumes) |
| `storageCapacity` | true: pod scheduling considers CSIStorageCapacity objects published for the driver |
| `tokenRequests` | kubelet passes the pod's bound service account tokens for these audiences in `volume_context` of `NodePublishVolume` (audiences must be distinct; `""` means the kube-apiserver audience) |
| `requiresRepublish` | true: kubelet periodically calls `NodePublishVolume` (short-lived volumes, token refresh); drivers must only update volume contents atomically |
| `seLinuxMount` | true: the driver's volumes can each be mounted with a different SELinux label via `-o context=<label>` (needs the `SELinuxMountReadWriteOncePod` feature gate); default false |

## Changes
Per the `storage.k8s.io/v1` API types: `attachRequired` and `volumeLifecycleModes` are immutable;
`podInfoOnMount` and `fsGroupPolicy` (mutable since 1.29) and `storageCapacity` (mutable since 1.22) can be updated in place.
A CSIDriver object should exist for the whole lifetime of all pods that use the driver's volumes.

## Verify
```bash
kubectl get csidrivers
kubectl get csidriver ebs.csi.aws.com -o yaml
kubectl get volumeattachments | head        # VolumeAttachment objects relate to drivers that require attach
```
Missing CSIDriver object: defaults apply, including `attachRequired: true`, so attach will be
called for a driver that does not implement it.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed against the kubernetes-csi CSIDriver object page and the storage.k8s.io/v1 CSIDriverSpec comments: field semantics, defaults (attachRequired true with or without a CSIDriver object, fsGroupPolicy ReadWriteOnceWithFSType, volumeLifecycleModes Persistent), fsGroupPolicy GA in 1.23, and mutability. Fixed the wrong claim that attachRequired became mutable: the API types say it is immutable (podInfoOnMount, fsGroupPolicy and storageCapacity are mutable). Removed examples (NFS, secrets-store) not stated in those pages.

Method: documentation only; no commands were run.
