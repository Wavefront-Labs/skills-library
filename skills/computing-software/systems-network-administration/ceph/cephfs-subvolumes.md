---
id: computing-software.systems-network-administration.ceph.cephfs-subvolumes
name: cephfs-subvolumes
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephfs, subvolume, subvolumegroup, volumes, authorize]
level: practitioner
status: docs-checked
description: "Manage CephFS volumes, subvolume groups and subvolumes, including size, authorisation and eviction."
sources:
  - https://docs.ceph.com/en/latest/cephfs/fs-volumes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Volumes:

```
ceph fs volume create <vol_name>
ceph fs volume ls
ceph fs volume info vol_name
```

Groups and subvolumes:

```
ceph fs subvolumegroup create <vol_name> <group_name> [--size <size_in_bytes>] [--pool_layout <data_pool_name>]
ceph fs subvolume create <vol_name> <subvol_name> [--size <size_in_bytes>] [--group_name <subvol_group_name>]
ceph fs subvolume resize <vol_name> <subvol_name> <new_size> [--group_name <subvol_group_name>] [--no_shrink]
ceph fs subvolume rm <vol_name> <subvol_name> [--group_name <subvol_group_name>] [--force] [--retain-snapshots]
```

Give a CephX ID access, list and evict:

```
ceph fs subvolume authorize <vol_name> <sub_name> <auth_id> [--group_name=<group_name>] [--access_level=<access_level>]
ceph fs subvolume authorized_list <vol_name> <sub_name>
ceph fs subvolume deauthorize <vol_name> <sub_name> <auth_id>
ceph fs subvolume evict <vol_name> <sub_name> <auth_id>
```

`--retain-snapshots` removes the subvolume but keeps its snapshots; without it, removal fails if the subvolume has snapshots. Removal moves the subvolume to a trash folder and purges it asynchronously. `--force` lets removing a non-existent subvolume succeed. Retained snapshots can be clone sources.

`ceph fs subvolume authorize` takes `--access_level` of `r` or `rw`. `ceph fs volume create` creates a file system with its data and metadata pools; the metadata pool must be replicated. The size of a group or subvolume is set as a quota.

Create options include `--pool_layout`, `--uid`, `--gid`, `--mode` and `--namespace-isolated`. By default a subvolume has mode 755 and takes UID and GID from its group, and a group defaults to mode 755, UID 0 and GID 0. With a namespace-isolated group, the group directory sits in RADOS namespace `fsvolumens__<group>` and every subvolume inherits isolation with its own `fsvolumens__<group>_<subvolume>` namespace. An earmark tags a subvolume for a service such as NFS or SMB. `ceph fs subvolume resize` takes sizes like `100KiB` (strictly cast to IEC units, so `1KB` is 1024 bytes), `inf` for unlimited, and `--no_shrink` blocks shrinking below the used size. `evict` removes clients based on the auth ID and the subvolume mounted. `ceph fs volume rename` is an expensive operation: the CephX IDs authorised for the old name must be reauthorised for the new one and mirroring must be disabled.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "FS Volumes and Subvolumes" on docs.ceph.com (volumes, subvolume groups, create, remove, resize, authorize, evict sections). Removed nothing; added the removal, access-level and resize details the page states.
