---
id: computing-software.systems-network-administration.ceph.rbd-image-lifecycle
name: rbd-image-lifecycle
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, image, create, resize, rm, rbd-pool-init]
level: intro
status: docs-checked
description: "Create, list, inspect, resize and remove RBD images, and prepare a pool and a user for block devices."
sources:
  - https://docs.ceph.com/en/latest/rbd/rados-rbd-cmds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prepare a pool and a limited user. Create the pool with the `ceph` tool, then initialise it for RBD:

```
rbd pool init <pool-name>
ceph auth get-or-create client.qemu mon 'profile rbd' osd 'profile rbd pool=vms, profile rbd-read-only pool=images' mgr 'profile rbd pool=images'
```

The `rbd` command uses the Ceph user ID `admin` unless told otherwise; the page recommends a user with fewer permissions. The output of `ceph auth get-or-create` is the keyring, which can be written to `/etc/ceph/ceph.client.{ID}.keyring`. Pass `--id {id}` to `rbd` to use another user.

Images:

```
rbd create --size {megabytes} {pool-name}/{image-name}
rbd ls {poolname}
rbd info {pool-name}/{image-name}
rbd resize --size 2048 foo
rbd resize --size 2048 foo --allow-shrink
rbd rm {pool-name}/{image-name}
```

For example `rbd create --size 1024 swimmingpool/bar` creates a 1 GB image `bar` in pool `swimmingpool`. If you give no pool, the image goes in the default pool `rbd`, and `rbd ls` lists that pool. A pool must be created before you can use it.

Images are thin provisioned: they use no physical storage until you save data, and `--size` only sets the maximum capacity. `rbd resize --size 2048 foo` increases an image; decreasing needs `--allow-shrink`.

The usual name form is `{pool-name}/{image-name}`, for example `rbd info swimmingpool/bar`. The page warns that other naming conventions, such as `userid/<uuid>`, might conflict and be confusing.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "Basic Block Device Commands" on docs.ceph.com. Removed: the advice to shrink only after reducing the file system and the statement that shrinking loses data past the new end, which the page does not state. Added the `mgr` cap that the page's user example includes.
