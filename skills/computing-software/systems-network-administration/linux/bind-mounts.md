---
id: computing-software.systems-network-administration.linux.bind-mounts
name: bind-mounts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, filesystems, bind-mount, rbind, read-only-bind, mount-propagation, fstab, chroot, lpic-1, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Use bind mounts to expose a directory at a second path: fstab entries, read-only binds (remount step), recursive rbind for chroots, propagation flags, and SELinux labels."
sources:
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc
  - https://github.com/systemd/systemd/blob/main/man/systemd.mount.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bind mounts

**Goal:** make a directory appear at another path (relocate `/var/lib/app` onto a big disk,
give an SFTP chroot access to a share, prepare a chroot for repair) without symlinks.

## 1. Basic
```bash
mount --bind /srv/data/app /var/lib/app
findmnt /var/lib/app            # show the mount
umount /var/lib/app
```
fstab:
```
/srv/data/app   /var/lib/app   none   bind   0 0
```
For ordering with the underlying mount use `x-systemd.requires-mounts-for=/srv/data` in options (systemd.mount(5)).

## 2. Read-only bind
```bash
mount --bind /srv/share /chroot/sftp/share
mount -o remount,bind,ro /chroot/sftp/share      # second step makes the bind read-only
mount -o bind,ro /srv/share /x                   # util-linux 2.27+ does both in one (not atomic: two syscalls)
```
The original path stays writable — `ro` applies to the new mount point only.

## 3. Recursive binds (chroot repair)
```bash
for d in dev proc sys run; do mount --rbind /$d /mnt/sysroot/$d; done
mount --make-rslave /mnt/sysroot/sys; mount --make-rslave /mnt/sysroot/dev   # stop propagation back to the host
chroot /mnt/sysroot /bin/bash
umount -R /mnt/sysroot
```
`--bind` doesn't include submounts; `--rbind` does.

## 4. Propagation
`findmnt -o TARGET,PROPAGATION` shows the flags. On a shared mount, mounts and unmounts propagate to its mirrors.
`--make-private`, `--make-slave`, `--make-shared`, `--make-unbindable` (r-prefixed for recursive) control it — relevant for containers and chroots.

## Gotchas
- `du` and backup tools see the data twice; exclude bind targets.
- A single **file** can be bind-mounted onto another file (`mount --bind file1 file2`).
- Unmount order: binds before the underlying filesystem.

## Verify
- [ ] `findmnt <target>` shows the bind with the expected source and `ro` if intended.
- [ ] `touch` in a read-only bind fails with "Read-only file system" while the source stays writable.
- [ ] After reboot the bind is present (`mount -a` clean).

## Checked

2026-10-26. util-linux master (last commit 2026-10-26) mount(8): --bind and --rbind (bind attaches no submounts), single-file bind, read-only bind via remount,bind,ro, one-step bind,ro since util-linux 2.27 (non-atomic), propagation flags and findmnt -o TARGET,PROPAGATION. systemd.mount(5): x-systemd.requires-mounts-for=. Removed unconfirmed remarks about fstab ro handling, systemd making / shared, findmnt SOURCE format, SELinux labels and editors breaking file binds.

Method: documentation only; no commands were run.
