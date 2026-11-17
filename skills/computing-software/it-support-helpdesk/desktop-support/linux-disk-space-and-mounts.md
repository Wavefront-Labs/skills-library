---
id: computing-software.it-support-helpdesk.desktop-support.linux-disk-space-and-mounts
name: linux-disk-space-and-mounts
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, linux-client, linux-disk-space, df, du, ncdu, fstab, mount, lsblk, inodes, journal-vacuum, deleted-open-files, comptia-a-plus]
level: practitioner
status: draft
description: "Free space and fix mounts on Linux desktops: df/du/ncdu, inode exhaustion, journal and package cache cleanup, deleted-but-open files, and safe fstab entries for shares and disks."
sources:
  - "https://man7.org/linux/man-pages/man5/fstab.5.html"
  - "https://www.freedesktop.org/software/systemd/man/latest/journalctl.html"
  - "https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# linux-disk-space-and-mounts

Goal: a full disk is diagnosed in minutes and cleaned without deleting the
wrong thing; mounts come back after reboot and don't hang boot.

## Where is the space
```bash
df -h                    # per filesystem
df -i                    # inodes: 100% IUse with free space = millions of tiny files
sudo du -xh --max-depth=1 / | sort -h | tail
ncdu -x ~               # interactive, if installed (user's home)
lsblk -f                 # disks, partitions, filesystems, mountpoints
```

## Safe cleanups
```bash
sudo journalctl --vacuum-size=200M
sudo apt clean && sudo apt autoremove --purge     # Debian/Ubuntu
sudo dnf clean all                                # Fedora/RHEL
snap list --all | awk '/disabled/{print $1, $3}'  # old snap revisions, remove with snap remove --revision
docker system df; docker system prune             # dev machines - ask first
rm -rf ~/.cache/*                                 # per-user caches (close apps first)
```
Trash: `~/.local/share/Trash`. Old kernels are handled by autoremove.

## Space not freed after deleting
A process still holds the deleted file open:
```bash
sudo lsof +L1      # deleted files still open, with size and PID
```
Restart that process (often a log writer) to release space.

## Mounts
- Network share at boot, without hanging if offline:
  ```
  //fs01/shared  /mnt/shared  cifs  credentials=/etc/smb-cred,uid=1000,_netdev,nofail,x-systemd.automount  0  0
  ```
  `nofail` + `x-systemd.automount` = mount on first access, boot doesn't
  wait. Credentials file mode 600.
- Extra disk: use `UUID=` from `lsblk -f`, never `/dev/sdb1` (names change).
- Test before reboot: `sudo mount -a` (errors here = boot problems later);
  `findmnt --verify`.
- A bad fstab line drops boot to emergency mode — fix from that shell
  (`mount -o remount,rw /`, edit, reboot).

## Gotchas
- `/boot` filling up (separate small partition) blocks kernel updates —
  remove old kernels with the package manager, not `rm`.
- Btrfs (Fedora default): `df` can mislead; use `btrfs filesystem usage /`.
  Snapshots (Timeshift/snapper) can hold lots of space.

## Verify
`df -h` shows healthy headroom (> 15 %), `sudo mount -a` returns silently,
and the share is present after a reboot.
