---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.weed-mount-fuse-basics
name: weed-mount-fuse-basics
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-mount, fuse, mountpoint]
level: practitioner
status: docs-checked
description: "Mount a SeaweedFS filer path as a local POSIX filesystem with weed mount: options, supported operations, xattr, unmounting and non-root pitfalls."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/FUSE-Mount
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# weed mount fuse basics

```bash
weed mount -filer=localhost:8888 -dir=/mnt/seaweedfs -filer.path=/
weed mount -filer=localhost:8888 -dir=/mnt/chris -filer.path=/users/chris -collection=chris
weed mount -filer=localhost:8888 -dir=/mnt/seaweedfs -volumeName=Photos
```
Supported: read/write, create, mkdir, list, remove, rename, chmod, chown, symlinks, hard links, free-space reporting, copy_file_range, lseek, advisory locks (flock and fcntl byte-range), extended attributes.

Architecture: the mount keeps a connection to the master for volume locations and syncs metadata from the filer, so directory listings are local; reads go to volume servers directly, writes upload chunks then record metadata in the filer.

Mount subtype: `cp weed /sbin/mount.weed` then `mount -t weed fuse /mnt -o "filer=localhost:8888,filer.path=/"`. For several filers quote the list: `filer='ip1:8888,ip2:8888'`.

Troubleshooting:
- Stale mount: `sudo umount -f /mnt/seaweedfs` (or `-l`; on macOS `diskutil unmount force`).
- Non-root user: grant capabilities with `setcap`, and use `-allowOthers=false`.
- `df` shows cluster space consumed (replicas and EC shards counted); `-df.logical` reports logical data sizes.

Verify: `ls /mnt/seaweedfs` matches the filer listing.

## Checked
Checked 2026-11-09: the supported-operations list, the three mount examples, the mount.weed subtype and multi-filer quoting, the architecture description, unmount commands, the setcap/allowOthers workaround and the df/-df.logical behaviour all match the FUSE-Mount page. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page FUSE-Mount, read in full from a local clone of the wiki.
