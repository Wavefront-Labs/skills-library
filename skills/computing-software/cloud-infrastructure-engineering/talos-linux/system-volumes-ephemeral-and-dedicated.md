---
id: computing-software.cloud-infrastructure-engineering.talos-linux.system-volumes-ephemeral-and-dedicated
name: system-volumes-ephemeral-and-dedicated
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [volumeconfig, ephemeral, etcd, kubelet, cri, log, imagecache, mount-secure, provisioning]
level: advanced
status: docs-checked
description: "Tune Talos system volumes with VolumeConfig: limit or relocate EPHEMERAL, put ETCD, CRI, KUBELET or LOG on dedicated partitions, mount.secure, first-provisioning-only rule."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/disk-management/system.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported system volumes: `STATE`, `EPHEMERAL`, `IMAGECACHE`, `ETCD`, `CRI`, `KUBELET`, `LOG`. `EPHEMERAL` (`/var`) holds container data, images, logs and etcd data; it sits on the system disk, minimum 2 GiB, growing to fill the disk. `ETCD`, `CRI`, `KUBELET` and `LOG` are directories under it by default.

Configuration only applies while a volume has not yet been provisioned, and the backing (directory versus dedicated partition) is permanent. These `VolumeConfig` documents must be present at node provisioning.

```yaml
apiVersion: v1alpha1
kind: VolumeConfig
name: EPHEMERAL
provisioning:
  maxSize: 40GiB
```

Place EPHEMERAL on another disk:

```yaml
apiVersion: v1alpha1
kind: VolumeConfig
name: EPHEMERAL
provisioning:
  diskSelector:
    match: disk.transport == 'nvme' && !system_disk
```

A dedicated partition (optionally encrypted) isolates a component so it cannot fill `/var`, allows per-component limits, and lets you use a separate disk:

```yaml
apiVersion: v1alpha1
kind: VolumeConfig
name: KUBELET
provisioning:
  minSize: 1GB
  maxSize: 5GB
```

The same works for `ETCD` with a `diskSelector` and `minSize: 2GB`.

Mount options: EPHEMERAL stays executable with `nosuid` and `nodev`, inherited by directory-backed volumes. Dedicated partitions take `mount.secure` (default on: `nosuid`, `nodev`); for dedicated `ETCD` and `LOG` it also adds `noexec`, while `CRI` and `KUBELET` stay executable. `mount: secure: false` clears these.

`IMAGECACHE` exists only when the Image Cache feature is enabled.

## Checked

2026-11-04. Volume list, immutability of backing, YAML examples and mount.secure semantics confirmed on the System Volumes page.

Method: documentation only; no commands were run.
