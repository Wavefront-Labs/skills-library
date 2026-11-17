---
id: computing-software.cloud-infrastructure-engineering.kubernetes.volumeattributesclass-modify-iops
name: volumeattributesclass-modify-iops
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, storageclass, volumeattributesclass, csi, storage-performance]
level: practitioner
status: docs-checked
description: "Change a volume's IOPS, throughput or tier online with VolumeAttributesClass, driver support, PVC status fields, and rollback when modification fails."
sources: ["https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/modify-volume.md", "https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scope-volume-attributes-class"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VolumeAttributesClass

Lets you change mutable volume attributes (what the CSI driver exposes, for example IOPS or throughput) of an
existing PVC without recreating it. Beta since 1.31, GA in 1.34 (`storage.k8s.io/v1`; users can still disable it).

## Requirements
- A CSI driver that implements the `ModifyVolume` API (`ControllerModifyVolume`), for example the AWS EBS CSI driver
  (see its modify-volume doc); check each driver's docs.
- The `external-resizer` sidecar implements modification and `external-provisioner` handles provisioning with a
  class. The EBS driver docs list the `VolumeAttributesClass` feature gate on the API server, controller manager,
  scheduler and both sidecars as a requirement on clusters where it is not already on.

## Define classes
```yaml
apiVersion: storage.k8s.io/v1
kind: VolumeAttributesClass
metadata: {name: gp3-fast}
driverName: ebs.csi.aws.com
parameters:
  iops: "8000"
  throughput: "500"
```
Parameters are driver-specific; the parameters of an existing class are immutable (create a new class instead), while
the class name on a PVC can change. A class has at most 512 parameters and 256 KiB in total.

## Use
```yaml
kind: PersistentVolumeClaim
spec:
  storageClassName: gp3
  volumeAttributesClassName: gp3-fast
```
Changing `volumeAttributesClassName` on a PVC makes the CSI driver update the volume with the new class's attributes.

## Status
```bash
kubectl get pvc data -o jsonpath='{.status.currentVolumeAttributesClassName}{" "}{.status.modifyVolumeStatus}{"\n"}'
kubectl describe pvc data      # events at the end
```
`modifyVolumeStatus.status`: `Pending` (cannot be modified yet because of unmet requirements, such as the class not
existing), `InProgress` (volume is being modified), `Infeasible` (rejected as invalid by the CSI driver; reset
`volumeAttributesClassName` to its previous value to cancel, or specify a valid class).

## Gotchas
- Cloud-side modification limits can still apply; read your driver's and cloud's documentation.
- ResourceQuota can restrict class usage per namespace (a `VolumeAttributesClass` quota scope used with
  `scopeSelector`).
- Which attributes the driver can change, and what happens to parameters omitted from a new class, depends on the driver.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: GA in 1.34, beta 1.31 (VolumeAttributesClass feature-gate page: alpha 1.29, beta 1.31, stable 1.34), CSI-only with the ModifyVolume API, driverName/parameters shape, immutable class parameters with mutable PVC class name, 512 parameter/256 KiB limit, modifyVolumeStatus meanings and cancel-by-reverting (core/v1 types), quota scope, and EBS driver requirements. Removed the unconfirmed EBS 'one modification per 6 hours' claim, the GCP Hyperdisk example and the cooldown reading of Pending.

Method: documentation only; no commands were run.
