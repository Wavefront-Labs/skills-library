---
id: computing-software.cloud-infrastructure-engineering.kubernetes.default-storageclass-selection-and-change
name: default-storageclass-selection-and-change
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, default-storageclass, is-default-class, storageclass, dynamic-provisioning, cka]
level: practitioner
status: docs-checked
description: "Set or change the cluster's default StorageClass safely: the is-default-class annotation, multiple-default behaviour, retroactive assignment, and addon managers reverting you."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/", "https://kubernetes.io/docs/concepts/storage/storage-classes/#default-storageclass", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#retroactive-default-storageclass-assignment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default StorageClass selection and changing it

## How the default works
The `DefaultStorageClass` admission plugin fills `storageClassName` on PVCs that **omit** it,
using the class annotated `storageclass.kubernetes.io/is-default-class: "true"`.
- `storageClassName` omitted (nil): gets the default.
- `storageClassName: ""`: explicitly no class; binds only to pre-created PVs without a class.

## Change the default
```bash
kubectl get sc                                         # "(default)" marker
kubectl patch sc gp2 -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
kubectl patch sc gp3 -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
kubectl get sc
```
Existing PVCs keep their class; only new PVCs change.

## Behaviours worth knowing
- **Multiple defaults**: Kubernetes uses the most recently created default StorageClass for a
  PVC without `storageClassName`. Multiple defaults are allowed to enable seamless migration;
  keep only one.
- **No default**: a PVC created without `storageClassName` is accepted and its
  `storageClassName` stays unset until a default becomes available. Retroactive default
  assignment is stable since Kubernetes 1.28: the control plane then sets the default class
  on existing PVCs without a class, without recreation.
- **Addon managers can revert you**: depending on the installation method, a default
  StorageClass may be deployed and re-created by an addon manager. Consult your installation's
  documentation for how to disable individual addons.

## Choosing the default
- Use `volumeBindingMode: WaitForFirstConsumer` so zonal disks are created where the pod lands.
- Set `allowVolumeExpansion: true`.
- Dynamically provisioned PVs take the StorageClass `reclaimPolicy` (default `Delete`); use a
  separate named class with `reclaimPolicy: Retain` for data you must keep.

## Verify
```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: default-sc-test}
spec: {accessModes: [ReadWriteOnce], resources: {requests: {storage: 1Gi}}}
EOF
kubectl get pvc default-sc-test -o jsonpath='{.spec.storageClassName}'; kubectl delete pvc default-sc-test
```
Re-check a day later to catch an addon manager flipping it back.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: DefaultStorageClass admission behaviour and the is-default-class annotation, patch commands from the task page, newest default used when several exist, empty-string class semantics, retroactive default assignment stable since v1.28, and addon managers re-creating defaults. Removed the unconfirmed '1.26' version gate and claim that older clusters rejected PVCs, the per-vendor addon details and the custom-columns command. Kept the Reclaim default (Delete) claim for dynamic provisioning, which the PV docs state; the WaitForFirstConsumer and allowVolumeExpansion suggestions are advice, not version-specific facts.

Method: documentation only; no commands were run.
