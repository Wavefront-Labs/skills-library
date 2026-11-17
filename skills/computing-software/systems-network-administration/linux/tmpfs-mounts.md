---
id: computing-software.systems-network-administration.linux.tmpfs-mounts
name: tmpfs-mounts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, filesystems, tmpfs, tmp-on-tmpfs, dev-shm, ramdisk, tmp-mount, size-limit, fstab, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Use tmpfs deliberately: size and inode limits, /tmp on tmpfs via tmp.mount, /dev/shm sizing, mode/uid options, noexec hardening, and how tmpfs memory shows up in free."
sources:
  - https://docs.kernel.org/filesystems/tmpfs.html
  - https://www.freedesktop.org/software/systemd/man/latest/tmpfiles.d.html
  - https://www.freedesktop.org/wiki/Software/systemd/APIFileSystems/
  - https://docs.kernel.org/filesystems/tmpfs.html
  - https://github.com/systemd/systemd/blob/main/units/tmp.mount
  - https://github.com/systemd/systemd/blob/main/tmpfiles.d/tmp.conf
  - https://github.com/systemd/systemd/blob/main/man/logind.conf.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tmpfs

**Goal:** fast RAM-backed scratch space that can't eat all memory, and knowing which system
paths already are tmpfs.

## 1. Mount
```bash
mount -t tmpfs -o size=2G,mode=1777,nr_inodes=1M tmpfs /scratch
mount -o remount,size=4G /scratch          # resize live
df -h -t tmpfs
```
fstab:
```
tmpfs  /scratch  tmpfs  size=2G,mode=1777,nosuid,nodev,noexec  0 0
```
Options: `size=` (bytes, suffixes, or `%` of RAM; default 50 %), `nr_inodes=` (default half the number of physical RAM pages), `mode=`,
`huge=within_size` (THP), `noswap` (disables swap for the instance). A tmpfs cannot be resized below its current usage.
tmpfs memory can be swapped (unlike ramfs) and is only used as files are written.

## 2. /tmp on tmpfs
```bash
systemctl enable --now tmp.mount       # mounts tmpfs on /tmp
systemctl cat tmp.mount                # upstream unit: Options=mode=1777,strictatime,nosuid,nodev,size=50%%,nr_inodes=1m,x-systemd.graceful-option=usrquota
systemctl edit tmp.mount               # [Mount] Options=mode=1777,nosuid,nodev,noexec,size=4G
```
Consider: large unpacks/builds (`/tmp` is RAM-limited), software that expects /tmp to survive
reboots (shouldn't), and `noexec` breaking installers that run scripts from /tmp
(set `TMPDIR` for them). Cleanup policy for disk-backed /tmp lives in `tmpfiles.d`
(upstream `tmp.conf`: `q /tmp 1777 root root 10d`).

## 3. /dev/shm and /run
- `/dev/shm`: POSIX shared memory. Hardening: `nosuid,nodev,noexec` in fstab:
  `tmpfs /dev/shm tmpfs defaults,nosuid,nodev,noexec 0 0` (check that your applications still work).
- `/run/user/UID`: size limit set by `RuntimeDirectorySize=` in logind.conf (see logind.conf(5) for the default).

## 4. Memory accounting
tmpfs usage counts as `Shmem` and in `buff/cache` of `free`, but **is not reclaimable** while
files exist (only swappable). A full `/dev/shm` or `/tmp` tmpfs can cause OOM with "lots of
cache". Check `df -h -t tmpfs` when memory doesn't add up.

## Gotchas
- Sum of all tmpfs `size=` limits can exceed RAM — limits are caps, not reservations; set them so worst case still fits RAM+swap.
- Contents vanish on reboot/unmount — never point databases/queues there by accident.

## Verify
- [ ] `findmnt -t tmpfs` lists the intended mounts with size and flags.
- [ ] Writing beyond `size=` fails with "No space left on device" rather than OOM.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (filesystems/tmpfs), and the systemd sources `units/tmp.mount`, `tmpfiles.d/tmp.conf` and `logind.conf(5)` on 2026-10-26. Confirmed: `size=` default 50%, `nr_inodes` default, `mode=`, `huge=within_size`, `noswap`, remount resize with the below-usage limit, the upstream tmp.mount options and the `tmp.conf` `q /tmp 1777 root root 10d` line, `RuntimeDirectorySize=` exists. Removed: distribution default claims for tmp.mount, the noswap kernel-version claim, `/run` percentage, Docker flag, container accounting claim.

Method: documentation only; no commands were run.
