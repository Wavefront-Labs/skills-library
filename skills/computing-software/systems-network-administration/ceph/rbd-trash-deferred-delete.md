---
id: computing-software.systems-network-administration.ceph.rbd-trash-deferred-delete
name: rbd-trash-deferred-delete
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, trash, restore, deferred-delete, image-id]
level: practitioner
status: docs-checked
description: "Move RBD images to the trash for deferred deletion, list them, restore or permanently remove them."
sources:
  - https://docs.ceph.com/en/latest/rbd/rados-rbd-cmds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instead of deleting an image outright, defer-delete it by moving it to the trash:

```
rbd trash mv {pool-name}/{image-name}
rbd trash ls {poolname}
```

The listing shows the image ID (for example `2bf4474b0dc51`). Use the ID to restore or remove:

```
rbd trash restore {pool-name}/{image-id}
rbd trash restore swimmingpool/2bf4474b0dc51 --image new-name
rbd trash rm {pool-name}/{image-id}
```

`--image new-name` renames the image while restoring it.

Rules from the page:

- You can move an image to the trash even if it has snapshots or is in use by clones, but you cannot remove it from the trash under those conditions.
- `--expires-at` sets the deferment time (default is now). If that time has not yet arrived, you cannot remove the image unless you use `--force`.
- `rbd trash ls` with no pool lists the default pool `rbd`; `rbd trash restore {image-id}` restores into the default pool without naming it.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "Basic Block Device Commands" on docs.ceph.com (trash sections). Removed: the retention-flow advice and the claim that plain `rbd rm` has no recovery path, which the page does not state.
