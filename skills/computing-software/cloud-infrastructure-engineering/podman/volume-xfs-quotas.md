---
id: computing-software.cloud-infrastructure-engineering.podman.volume-xfs-quotas
name: volume-xfs-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [volume-quota, xfs, pquota, project-id, xfs-quota, size, inodes]
level: sme
status: docs-checked
description: "Enforce Podman volume size and inode limits with XFS project quotas: pquota mount, unique project IDs, xfs_quota setup with /etc/projects and /etc/projid."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-volume-create.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make size and inodes limits work on built-in volumes.

Podman uses XFS project quota controls for the size and the number of inodes of built-in volumes. The directory storing volumes must be on an XFS file system mounted with `pquota`; the example entry is `/dev/podman/podman-var /var xfs defaults,x-systemd.device-timeout=0,pquota 1 2`. For `size` and `inodes` on xfs, the page also says xfs must be mounted with the `prjquota` flag (see xfs_quota(8)) or Podman errors.

Podman generates a project ID per built-in volume at random, and IDs must be unique across the XFS file system, so overlap with other quotas is possible. Assign IDs to the storage directories using xfs_quota with offsets:

```
echo 100000:/var/lib/containers/storage/overlay >> /etc/projects
echo 200000:/var/lib/containers/storage/volumes >> /etc/projects
echo storage:100000 >> /etc/projid
echo volumes:200000 >> /etc/projid
xfs_quota -x -c 'project -s storage volumes' /<xfs mount point>
```

This gives containers IDs of 100000 and above and volumes 200000 and above, preventing conflicts with containers/storage.

## Checked
2026-11-09: read the QUOTAS section of the podman-volume-create man page and confirmed the XFS and pquota requirement, the fstab example, random project IDs, the /etc/projects and /etc/projid commands and the offsets. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

