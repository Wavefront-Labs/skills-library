---
id: computing-software.cloud-infrastructure-engineering.kubernetes.raw-block-volumes-for-databases
name: raw-block-volumes-for-databases
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, local-raw-block-volumes, block-volume-database, volumemode-block, volumedevices, databases]
level: practitioner
status: docs-checked
description: "Give storage engines raw block devices with volumeMode Block and volumeDevices, and know the device path rules and when a filesystem is the better choice."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#raw-block-volume-support", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#volume-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw block volumes

`volumeMode: Block` presents a volume to the Pod as a raw block device with no filesystem. The docs describe it as the fastest possible access path, and say the application must know how to handle a raw block device. `Filesystem` is the default; with `Filesystem` mode an empty block device is formatted before first mount. Block mode is stable since 1.18 and supported by CSI (including some migrated types), FC, iSCSI and local volumes.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: data-0}
spec:
  volumeMode: Block
  storageClassName: <csi-storage-class>
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 500Gi}}
---
apiVersion: v1
kind: Pod
metadata: {name: engine}
spec:
  containers:
  - name: db
    image: <engine-image>
    volumeDevices:                  # not volumeMounts
    - {name: data, devicePath: /dev/xvdb}
  volumes:
  - name: data
    persistentVolumeClaim: {claimName: data-0}
```
Specify a device path in the container instead of a mount path. In a StatefulSet put `volumeMode: Block` in the `volumeClaimTemplates` entry.

## Gotchas
- The storage class/driver must support block mode; a PV and PVC must agree on `volumeMode` to bind (see Binding Block Volumes in the PV docs).
- There is no filesystem, so filesystem tools such as `df` do not apply; monitor through the engine or node-level device statistics.
- Windows nodes cannot attach raw block devices to Pods.
- Run a permissions test under your Pod Security level; device access and ownership depend on the driver and node.

## Verify
`kubectl exec <pod> -- ls -l /dev/xvdb` shows a block device the process can open.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: volumeMode Block, volumeDevices and devicePath, supported plugin types, stable since 1.18.

Method: documentation only; no commands were run.
