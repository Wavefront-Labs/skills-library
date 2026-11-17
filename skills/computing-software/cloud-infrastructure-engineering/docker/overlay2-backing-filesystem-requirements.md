---
id: computing-software.cloud-infrastructure-engineering.docker.overlay2-backing-filesystem-requirements
name: overlay2-backing-filesystem-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, overlay2, storage-driver, ftype, d-type, xfs, backing-filesystem]
level: advanced
status: docs-checked
description: "Check the filesystem under /var/lib/docker supports overlay2: ext4 or xfs with ftype=1 (d_type), what fails on NFS, ZFS or old xfs, and how to fix it with a new volume."
sources: ["https://docs.docker.com/engine/storage/drivers/overlayfs-driver/", "https://docs.docker.com/engine/storage/drivers/select-storage-driver/#supported-backing-filesystems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# overlay2 backing filesystem requirements

overlay2 stacks directories from the filesystem holding the data root. That filesystem must
support `d_type` (file type in directory entries).

## Supported backing filesystems for overlay2
Docker lists `xfs` with `ftype=1`, `ext4`, `btrfs` (and more) as supported backing
filesystems for `overlay2`. On `xfs`, overlay2 requires `d_type=true`; verify with `xfs_info`
(the `ftype` option must be `1`) and format with `-n ftype=1`.

## Check
```bash
docker info | grep -A3 'Storage Driver'
#  Storage Driver: overlay2
#   Backing Filesystem: xfs
#   Supports d_type: true
xfs_info /var/lib/docker                    # ftype=1 required
```
`docker info` reports the backing filesystem and `Supports d_type`; the docs require
`d_type=true` for overlay2 on xfs. The `vfs` driver is not a union filesystem: each layer is a
full copy of the directory.

## Fix: a properly formatted volume
```bash
sudo systemctl stop docker docker.socket containerd
sudo mkfs.xfs -n ftype=1 /dev/nvme1n1
sudo mkdir -p /mnt/docker-data
echo '/dev/nvme1n1 /mnt/docker-data xfs defaults,pquota 0 0' | sudo tee -a /etc/fstab
sudo mount /mnt/docker-data
sudo rsync -aHAX /var/lib/docker/ /mnt/docker-data/
# then set "data-root": "/mnt/docker-data" in /etc/docker/daemon.json (merge with existing keys)
sudo systemctl start docker
```
`pquota` mount option enables per-container size limits (`--storage-opt size=`) on xfs.

## Other layouts
| Host situation | Approach |
|---|---|
| Root on ZFS | the `zfs` driver requires `zfs` as the backing filesystem |
| Root on btrfs | `overlay2` lists `btrfs` as a supported backing filesystem; the `btrfs` driver requires `btrfs` |
| containerd image store | Uses the `overlayfs` snapshotter by default |

## Gotchas
- Changing the storage driver makes existing containers and images inaccessible.
- `fuse-overlayfs` is only needed for rootless Docker on hosts without rootless `overlay2`; it
  is not needed since Linux kernel 5.11.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine overlayfs driver and storage driver selection pages (docker/docs main).
Confirmed: overlay2 backing filesystems (`xfs` with ftype=1, `ext4`, `btrfs`, and more), the xfs `d_type=true`/`ftype=1`
requirement and `xfs_info` check, `mkfs.xfs -n ftype=1`, mounting a separate backing filesystem at `/var/lib/docker`,
vfs not being a union filesystem, changing drivers hiding existing data, fuse-overlayfs and kernel 5.11, default `overlayfs`
containerd snapshotter. Removed: the claims that NFS, CIFS and FUSE cannot back overlay2, the d_type-false behaviour of
older and newer Engines, the ZFS and btrfs workaround layouts, the inode-exhaustion advice and the containerd
data path, which the documentation does not state.

Method: documentation only; no commands were run.
