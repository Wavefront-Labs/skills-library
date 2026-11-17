---
id: computing-software.systems-network-administration.ceph.cephfs-client-authorize
name: cephfs-client-authorize
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephfs, client, authorize, path-restriction, caps]
level: practitioner
status: docs-checked
description: "Authorise a CephX client for one CephFS path with ceph fs authorize."
sources:
  - https://docs.ceph.com/en/latest/cephfs/client-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a user limited to a file system and path:

```
ceph fs authorize <fs_name> client.<client_id> <path-in-cephfs> rw
ceph fs authorize cephfs_a client.foo / r /bar rw
```

Multiple path and access pairs can follow. That second example gives read on `/` and read-write on `/bar`.

Mount a restricted client at its directory:

```
ceph-fuse -n client.foo mnt -r /bar
```

Optional restrictions described on the page: the `p` flag for layout and quota changes, the `s` flag for snapshots, network restriction, and file system information restriction. For the last, compare what a restricted user can list:

```
ceph fs ls
ceph fs authorize cephfs client.someuser / rw
ceph fs ls -n client.someuser -k ceph.client.someuser.keyring
```

Save the keyring with `ceph auth get client.someuser > ceph.client.someuser.keyring`.

Capability flags: `p` allows setting layouts and quotas in addition to `rw`, and `s` allows creating or deleting snapshots. All flags except `rw` must be in alphabetical order, so `s` follows `p`. For example `allow rw, allow rws path=/bar` lets a client snapshot only in `/bar`. Add a network restriction in CIDR form, as in `allow r network 10.0.0.0/8`, to confine a client to that network. `root_squash` stops clients with uid 0 or gid 0 from write operations such as `rm`, `rmdir`, `mkdir`, `mksnap` and `rmsnap`, while reads are allowed; for example `ceph fs authorize a client.test_a / rw root_squash /volumes rw`.

## Checked

2026-11-09. Confirmed against: the Ceph CephFS Client Capabilities page (docs.ceph.com/en/latest/cephfs/client-auth/): path restriction, p and s flags, network restriction, file system information restriction and root_squash.

Removed: the claim that quotas on a restricted client need the quota directory visible (not on the page).

Method: documentation only; no commands were run.

