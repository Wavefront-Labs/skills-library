---
id: computing-software.systems-network-administration.ceph.rbd-snapshots-clones-flatten
name: rbd-snapshots-clones-flatten
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, snapshot, clone, flatten, protect, layering]
level: practitioner
status: docs-checked
description: "Snapshot an RBD image, roll back, protect a snapshot and clone it, then flatten the clone."
sources:
  - https://docs.ceph.com/en/latest/rbd/rbd-snapshot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snapshots:

```
rbd snap create rbd/foo@snapname
rbd snap ls rbd/foo
rbd snap rollback rbd/foo@snapname
rbd snap rm rbd/foo@snapname
rbd snap purge rbd/foo
```

Clones need a protected snapshot as parent:

```
rbd snap protect rbd/foo@snapname
rbd clone rbd/foo@snapname rbd/bar
rbd children rbd/foo@snapname
```

Flatten the clone, which copies the snapshot data into it and removes the reference to the parent, then unprotect:

```
rbd flatten rbd/bar
rbd snap unprotect rbd/foo@snapname
```

Notes:

- You cannot delete a protected snapshot. You may not unprotect and delete a snapshot that has clone references; flatten or delete each clone first.
- Rollback overwrites the current image with snapshot data and takes longer as the image grows. Cloning from a snapshot is faster and is the preferred way of returning to a pre-existing state.
- Flatten time increases with the size of the snapshot, and a flattened image takes more storage than a layered clone.
- Cloning works only for "RBD format 2" images (not created with `--image-format 1`); a snapshot can be cloned into a different pool.
- With CephX enabled (the default) pass `--id {user-ID} --keyring /path/to/secret` or `--name {username} --keyring ...`; the `CEPH_ARGS` environment variable avoids retyping them.
- Deleting a snapshot does not immediately free OSD capacity: OSDs delete asynchronously ("snaptrim", shown in `ceph status`).

Consistency: RBD is unaware of any file system inside an image, so snapshots are only crash-consistent unless coordinated with the operating system. Pause or stop I/O before a snapshot. Quiesce a file system with `fsfreeze`, and for virtual machines `qemu-guest-agent` can freeze file systems automatically at snapshot time. Snapshots taken without write quiescing could need an `fsck` pass before being mounted again.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "Snapshots" on docs.ceph.com. Added the format 2, snaptrim and cross-pool notes the page gives; removed nothing numeric.
