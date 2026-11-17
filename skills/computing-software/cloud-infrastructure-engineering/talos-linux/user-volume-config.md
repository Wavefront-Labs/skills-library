---
id: computing-software.cloud-infrastructure-engineering.talos-linux.user-volume-config
name: user-volume-config
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [uservolumeconfig, volumes, hostpath, disk-selector, volumestatus, wipe-disk, local-storage]
level: practitioner
status: docs-checked
description: "Provision a Talos user volume with UserVolumeConfig: naming and label rules, diskSelector and size bounds, mount under /var/mnt, hostPath use in pods, wipe disk removal."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/disk-management/overview.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/disk-management/user.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos models disks as volumes. Besides built-in system volumes, user volumes are a pool of allocatable local storage, mostly for Kubernetes `hostPath` mounts. Applying a `UserVolumeConfig` locates an existing volume or provisions one on a disk matching `diskSelector` with enough free space for `minSize`.

The name is 1 to 34 characters of ASCII letters, digits and `-`, unique across user volumes. The partition label is `u-<volume-name>` and the mount point is `/var/mnt/<volume-name>`, propagated into the `kubelet` container (so `subPath` mounts work). Encryption is optional.

```yaml
# user-volume.patch.yaml
apiVersion: v1alpha1
kind: UserVolumeConfig
name: local-volume
provisioning:
  diskSelector:
    match: disk.transport == 'nvme'
  minSize: 100GB
  maxSize: 200GB
```

```bash
talosctl --nodes <NODE> patch mc --patch user-volume.patch.yaml
talosctl get volumestatus u-local-volume # note u- prefix
talosctl get mountstatus
```

Use `-o yaml` on `volumestatus` if provisioning fails. In a pod, mount it with `hostPath: path: /var/mnt/local-volume`; the container path may differ.

**Removal.** Ensure no pod mounts it, then delete the document from the machine config; `VolumeStatus` and `MountStatus` disappear but data stays, so re-applying re-provisions the same disk. To wipe and free the space:

```bash
talosctl wipe disk nvme0n1p2 --drop-partition
```

Get the partition name from `VolumeStatus` before removal or from `DiscoveredVolume` later. The error `blockdevice is in use by volume` means the document is still in the machine config.

## Checked

2026-11-04. Naming rules, label and mount path, YAML, status commands, hostPath example and wipe procedure confirmed on the Overview and User Volumes pages.

Method: documentation only; no commands were run.
