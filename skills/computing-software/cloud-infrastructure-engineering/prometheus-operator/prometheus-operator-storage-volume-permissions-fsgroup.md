---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-storage-volume-permissions-fsgroup
name: prometheus-operator-storage-volume-permissions-fsgroup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [fsgroup, volume-permissions, security-context, nfs, cephfs, crashloop]
level: advanced
status: docs-checked
description: "Fix Prometheus crash loops on NFS or CephFS volumes by setting fsGroup, runAsUser and runAsNonRoot in the securityContext."
sources: ["https://prometheus-operator.dev/docs/platform/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Prometheus container runs as non-root `nobody` (UID 65534 in the default image), and the operator sets no pod security context unless you do. If the volume root is owned by `root` and not writable by others, which is common with NFS and CephFS file storage, Prometheus cannot write and the pod crash-loops.

## Fix
Set `fsGroup` so the kubelet changes group ownership when mounting:
```yaml
spec:
  securityContext:
    fsGroup: 65534
    runAsNonRoot: true
    runAsUser: 65534
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: my-file-storage
        resources:
          requests:
            storage: 40Gi
```
The same applies to `Alertmanager` and `ThanosRuler`. Adjust the IDs if your image runs as another user.

## Limits
Whether `fsGroup` takes effect depends on the volume type, and for CSI volumes on the driver `fsGroupPolicy` (see the Kubernetes docs on volume permission and ownership change policy). When it is ignored, as with plain NFS, make the directory writable by the container user on the storage side.

For hostPath volumes the same securityContext is shown together with a PV using `hostPath.path` and `persistentVolumeReclaimPolicy: Retain`; the container needs permission on that host path.

## Checked

2026-11-08. Read the storage page in full. Claims match; no changes needed.

Method: documentation only; no commands were run.
