---
id: computing-software.systems-network-administration.linux.overlayfs-mounts
name: overlayfs-mounts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, overlayfs, overlay-mount, lowerdir, upperdir, workdir, container-storage, read-only-root]
level: advanced
status: docs-checked
description: "Build overlayfs mounts: lowerdir/upperdir/workdir rules, multiple read-only lowers, whiteouts, use for writable layers over read-only roots, and common mount errors."
sources:
  - https://docs.kernel.org/filesystems/overlayfs.html
  - https://man7.org/linux/man-pages/man8/mount.8.html
  - https://docs.kernel.org/filesystems/overlayfs.html
  - https://github.com/systemd/systemd/blob/main/man/systemd.mount.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# overlayfs

**Use:** a writable view over read-only data — container image layers, live systems, testing changes to a
directory you must not modify, kiosk/appliance read-only roots.

```bash
mkdir -p /srv/ovl/{upper,work,merged}
mount -t overlay overlay -o lowerdir=/srv/base,upperdir=/srv/ovl/upper,workdir=/srv/ovl/work /srv/ovl/merged
# multiple read-only lowers (leftmost is top):
mount -t overlay overlay -o lowerdir=/srv/patch:/srv/base /srv/ro-merged     # no upper = read-only overlay
```
fstab: `overlay /srv/ovl/merged overlay lowerdir=/srv/base,upperdir=/srv/ovl/upper,workdir=/srv/ovl/work,x-systemd.requires-mounts-for=/srv 0 0`.

## Semantics
- Reads come from upper if present, else lowers. Writes copy the file up to upper ("copy-up") first.
- Deleting a lower file creates a **whiteout** in upper (a character device 0/0, or a zero-size file with the `trusted.overlay.whiteout` xattr); a directory is made opaque with the `trusted.overlay.opaque` xattr.
- Discard changes: unmount, empty upper and work. Commit changes: rsync upper into base (handle whiteouts!).

## Rules / errors
- `workdir` must be a directory on the **same filesystem** as `upperdir`.
- The upper filesystem must support creating `trusted.*` and/or `user.*` extended attributes and provide valid `d_type` in readdir, so NFS is not suitable. A read-only overlay of read-only lowers may use any filesystem type.
- Changing the lower or upper directories while the overlay is mounted gives undefined behaviour (no crash or deadlock).
- For unprivileged use the `userxattr` mount option makes overlayfs use `user.overlay.*` xattrs instead of `trusted.overlay.*`.

## Verify
- [ ] Writing in `merged` creates files only in `upper`; the lower tree is unchanged.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (filesystems/overlayfs) on 2026-10-26. Confirmed: `lowerdir`/`upperdir`/`workdir` syntax, workdir on the same filesystem as upperdir, copy-up, whiteouts and opaque xattrs, upper filesystem xattr and `d_type` requirements, read-only overlay of lowers, undefined behaviour when layers change, `userxattr`. Removed: the XFS `ftype` claim, the module-error message text, the fuse-overlayfs and 5.11 claims. `x-systemd.requires-mounts-for` is a documented mount option (systemd.mount man source); lower layers stack right-to-left with the leftmost on top.

Method: documentation only; no commands were run.
