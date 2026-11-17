---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-persistent-storage
name: prometheus-operator-persistent-storage
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [persistent-storage, volumeclaimtemplate, storageclass, pvc, manual-pv, hostpath, emptydir]
level: practitioner
status: docs-checked
description: "Give Prometheus, Alertmanager and ThanosRuler persistent storage through volumeClaimTemplate, with dynamic provisioning or manually created PersistentVolumes."
sources: ["https://prometheus-operator.dev/docs/platform/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the operator uses `emptyDir`, which is lost when pods are redeployed. For persistence set `spec.storage.volumeClaimTemplate` on `Prometheus`, `Alertmanager` or `ThanosRuler`; each StatefulSet pod gets its own PVC.

## Dynamic provisioning
Create a `StorageClass` (the example uses `kubernetes.io/aws-ebs`, `type: gp2`; use fast, high-I/O volumes) and name it:
```yaml
spec:
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: ssd
        resources:
          requests:
            storage: 40Gi
```
With kube-prometheus use its jsonnet example instead of editing the resource.

## Manual provisioning
Use a label selector in the claim template plus a pre-created PersistentVolume carrying that label (for example an NFS volume with `accessModes: [ReadWriteOnce]`, which is required). A hostPath PV with `persistentVolumeReclaimPolicy: Retain` works too if the container can write the path.

## Default StorageClass trap
Cloud providers pre-install a default StorageClass that overrides manual provisioning, so claims will not bind to your PVs. Re-create the default class with the annotation `storageclass.kubernetes.io/is-default-class: "false"`.

See the volume permissions and resizing skills for the two usual follow-up problems.

## Checked

2026-11-08. Read the storage page in full. Claims match; no changes needed.

Method: documentation only; no commands were run.
