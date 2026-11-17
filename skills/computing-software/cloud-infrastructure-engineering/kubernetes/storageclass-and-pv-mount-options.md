---
id: computing-software.cloud-infrastructure-engineering.kubernetes.storageclass-and-pv-mount-options
name: storageclass-and-pv-mount-options
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, storageclass, mountoptions, nfs, csi, persistentvolume]
level: practitioner
status: docs-checked
description: "Set mountOptions on StorageClasses and PVs (NFS versions, noatime, discard), understand that they are not validated, and debug mounts that fail because of them."
sources: ["https://kubernetes.io/docs/concepts/storage/storage-classes/#mount-options", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#mount-options", "https://man7.org/linux/man-pages/man5/nfs.5.html", "https://github.com/kubernetes-csi/csi-driver-nfs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount options

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: nfs-fast}
provisioner: nfs.csi.k8s.io
parameters:
  server: nfs.example.internal
  share: /exports/k8s
mountOptions:
  - nfsvers=4.1
  - hard
```
Dynamically provisioned PVs get the `mountOptions` of their class. Static PVs set
`spec.mountOptions` themselves (supported volume types include `csi` (including CSI migrated types), `iscsi` and `nfs`).

## Rules
- Mount options are not validated on the class or the PV: if an option is invalid, the PV mount fails.
- If the volume plugin does not support mount options but they are specified, provisioning fails.
- A class's `mountOptions` apply to PVs dynamically created from it afterwards; they do not rewrite existing PVs.
- Not all PV types support mount options. The old annotation `volume.beta.kubernetes.io/mount-options` still works but is headed for deprecation.

## Useful options
Valid options depend on the volume type and driver. For NFS, `nfsvers=n` selects the protocol version,
`hard`/`soft` set recovery after request timeouts (`hard` is the default), `timeo`/`retrans` tune retries
and `nconnect=n` opens multiple connections (see nfs(5)). The `atime`/`noatime` options have no effect on NFS mounts.
For other drivers, use the options their documentation lists.

## Debug
```bash
kubectl describe pod <p>      # volume events at the end
kubectl logs -n <csi-namespace> <csi-node-pod> -c <driver-container>
```

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: mountOptions on StorageClass and PV, not validated, provisioning fails when the plugin lacks support, supported PV types, the legacy annotation, the NFS CSI driver's `server`/`share` parameters and `nfsvers=4.1` example, and nfs(5) semantics for nfsvers, hard, timeo, retrans and nconnect (noatime has no effect on NFS). Removed the unconfirmed block-device and SMB option table, rsize/wsize, kernel-version and node-shell debugging claims.

Method: documentation only; no commands were run.
