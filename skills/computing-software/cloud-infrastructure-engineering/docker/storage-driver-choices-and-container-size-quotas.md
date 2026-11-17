---
id: computing-software.cloud-infrastructure-engineering.docker.storage-driver-choices-and-container-size-quotas
name: storage-driver-choices-and-container-size-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, storage-driver, overlay2, btrfs-driver, zfs-driver, fuse-overlayfs, storage-opt-size, pquota, xfs-pquota]
level: advanced
description: "Choose between overlay2, btrfs, zfs and fuse-overlayfs, and cap a container's writable layer with --storage-opt size= using xfs project quotas."
sources: ["https://docs.docker.com/engine/storage/drivers/select-storage-driver/", "https://docs.docker.com/reference/cli/docker/container/run/#storage-opt", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/engine/storage/drivers/vfs-driver/", "https://docs.docker.com/engine/storage/containerd/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storage driver choices and per-container size quotas

## Choosing a driver
| Driver | When |
|---|---|
| `overlay2` | preferred driver on current Linux distributions; backing fs `xfs` with ftype=1, `ext4`, `btrfs` and more |
| `btrfs` | requires `btrfs` as the backing filesystem; supports snapshots but needs more setup and maintenance |
| `zfs` | requires `zfs` as the backing filesystem; docs call it a good choice for high-density workloads |
| `fuse-overlayfs` | only for rootless Docker on hosts without rootless `overlay2`; not needed since kernel 5.11 |
| `vfs` | intended for testing, or where no copy-on-write filesystem can be used; poor performance |
| containerd snapshotters | with the containerd image store (default snapshotter `overlayfs`; `stargz`, `soci`, `nydus` and `overlaybd` enable lazy pulling by default) |

```json
{ "storage-driver": "overlay2" }
```
Changing the storage driver makes existing images and containers inaccessible: save what you
need first, then switch and re-pull. For `btrfs` and `zfs`, prepare the backing filesystem
as described in the driver pages before setting `"storage-driver"`.

## Capping a container's writable layer
```sh
docker run --storage-opt size=10G app:1
```
`--storage-opt size=` is available only for the `btrfs`, `overlay2`, `windowsfilter` and `zfs`
storage drivers. For `overlay2` it requires the backing filesystem to be `xfs` mounted with the
`pquota` mount option; you can then pass any size less than the backing filesystem size. For
`windowsfilter`, `btrfs` and `zfs` you cannot pass a size below the Default BaseFS Size.

xfs setup: format with `-n ftype=1` and add `pquota` to the mount options (for example in
`/etc/fstab`) for the filesystem holding `/var/lib/docker`.

Daemon-wide default for overlay2: `"storage-opts": ["overlay2.size=20G"]` (documented as
`--storage-opt overlay2.size=1G` for `dockerd`; supported only on xfs with `pquota`).

## Gotchas
- The size option constrains the container filesystem; volumes and bind mounts are separate
  storage.

## Verify
`docker run --rm --storage-opt size=1G alpine sh -c 'dd if=/dev/zero of=/f bs=1M count=2000'`
fails once the writable layer reaches the limit; `docker info` shows the chosen driver.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine storage driver docs, `docker run` and `dockerd` references (docker/docs and docker/cli main).
Confirmed: driver descriptions and backing-filesystem table, fuse-overlayfs and kernel 5.11 note, vfs purpose,
`--storage-opt size` driver availability and the overlay2 xfs `pquota` requirement, `overlay2.size` as a `dockerd`
storage option, Default BaseFS Size limit for btrfs/zfs/windowsfilter, changing the driver making existing images and
containers inaccessible, containerd `overlayfs` default snapshotter and lazy-pull snapshotters. Removed: formatting and
`zpool` commands, the btrfs qgroup requirement, the exact kernel error text, the Compose `storage_opt` key and
the devicemapper row, none of which the documentation pages checked state.

Method: documentation only; no commands were run.
