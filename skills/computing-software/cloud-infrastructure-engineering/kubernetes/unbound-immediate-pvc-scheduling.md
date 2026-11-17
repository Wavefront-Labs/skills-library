---
id: computing-software.cloud-infrastructure-engineering.kubernetes.unbound-immediate-pvc-scheduling
name: unbound-immediate-pvc-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pending, unbound-immediate-pvc, pvc-pending, failedscheduling, volumebindingmode]
level: practitioner
status: docs-checked
description: "Fix pods Pending with 'pod has unbound immediate PersistentVolumeClaims': find why the PVC is not bound and when to switch to WaitForFirstConsumer."
sources: ["https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#binding", "https://github.com/kubernetes/kubernetes/blob/master/pkg/scheduler/framework/plugins/volumebinding/volume_binding.go", "https://github.com/kubernetes/kubernetes/blob/master/pkg/controller/volume/persistentvolume/pv_controller.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pod has unbound immediate PersistentVolumeClaims

## Meaning
The pod references a PVC that is not bound yet and does not use delayed binding (its StorageClass has
`volumeBindingMode: Immediate`, the default when unset, or it needs a static PV). The scheduler's VolumeBinding
plugin reports this reason and does not place the pod until the PVC binds.
```
0/3 nodes are available: pod has unbound immediate PersistentVolumeClaims. preemption: ...
```

## Find out why the PVC is Pending
```bash
kubectl get pvc <claim> -o wide
kubectl describe pvc <claim>      # Events at the end
```
| PVC event | Cause |
|---|---|
| `no persistent volumes available for this claim and no storage class is set` | no class set on the claim (and none applied as default) and no matching static PV |
| `storageclass.storage.k8s.io "fast" not found` (ProvisioningFailed) | typo or class missing |
| `Waiting for a volume to be created either by the external provisioner '<name>' or manually by the system administrator` | normal while the external provisioner works; if it persists, check the provisioner's logs |
| `ProvisioningFailed` with a driver error | the CSI driver or storage backend rejected the request (quota, bad parameters): read the message |
| no events, static PV expected | size, accessModes, volumeMode, storageClassName or selector mismatch with PVs |

```bash
kubectl get sc
kubectl logs -n <csi-namespace> <csi-controller-pod> -c <external-provisioner-container> --tail=50
kubectl get pv -o custom-columns=PV:.metadata.name,CAP:.spec.capacity.storage,MODES:.spec.accessModes,SC:.spec.storageClassName,STATUS:.status.phase
```

## Zonal storage
With Immediate binding, volumes are bound or provisioned without knowledge of the pod's scheduling
requirements, which may result in unschedulable pods (the scheduler then reports
`node(s) didn't match PersistentVolume's node affinity`). Use `WaitForFirstConsumer` for
topology-constrained storage so provisioning follows scheduling:
```yaml
volumeBindingMode: WaitForFirstConsumer
```
(StorageClass fields are immutable: create a new class and use it for new PVCs.)

## Verify
PVC Bound, then the pod is scheduled on a later scheduling attempt.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed in the scheduler VolumeBinding plugin and PV controller sources: the reason `pod has unbound immediate PersistentVolumeClaims`, the FailedBinding event `no persistent volumes available for this claim and no storage class is set`, the ExternalProvisioning event wording, and ProvisioningFailed events; in the docs: Immediate is the default and may produce unschedulable pods, StorageClass fields are immutable. Corrected the external-provisioner event wording (capital W, no comma) and the node affinity message. Removed the vendor-specific controller deployment name, the `sed` filter and the claim that class-less claims always mean no default exists.

Method: documentation only; no commands were run.
