---
id: computing-software.systems-network-administration.linux.swap-management
name: swap-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, swap, swap-file, swap-partition, swapon, swapoff, mkswap, swap-management, zram, zswap, swappiness, hibernation, resume, fallocate, btrfs-swap, storage, rhcsa, sysadmin, swap-priority]
level: practitioner
status: docs-checked
description: "Add, resize and remove swap on Linux: swap files vs partitions, fstab entries, zram/zswap, hibernation resume, and per-filesystem gotchas (Btrfs, sparse files)."
sources:
  - https://man7.org/linux/man-pages/man8/swapon.8.html
  - https://man7.org/linux/man-pages/man8/mkswap.8.html
  - https://docs.kernel.org/admin-guide/blockdev/zram.html
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-swapfile.rst
  - https://docs.kernel.org/admin-guide/sysctl/vm.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Swap management — files, partitions, zram, and not breaking hibernation

**Goal:** give the kernel swap space of the right size and kind, persistently, and know
when zram beats a disk-backed file.

## 1. Swap file (the default choice today)
```bash
fallocate -l 4G /swapfile          # preallocated files can be rejected as having holes on some filesystems; dd from /dev/zero is the most portable
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap defaults 0 0' >> /etc/fstab
swapon --show; free -h
```
- `chmod 600` keeps the swap file private (the Btrfs swapfile guide includes it in its steps).
- Priority: `swapon -p 10 …` / `pri=10` in fstab; higher is used first (0 to 32767; see swapon(8) and swapon(2) for how equal priorities behave).
- Remove: `swapoff /swapfile && rm /swapfile` and delete the fstab line. `swapoff` has to
  pull swapped pages back into RAM, so it needs enough free memory.

## 2. Swap partition / LV
```bash
lvcreate -L 8G -n swap vg0 && mkswap /dev/vg0/swap && swapon /dev/vg0/swap
echo '/dev/vg0/swap none swap defaults 0 0' >> /etc/fstab
```
Resize an LV-backed swap: `swapoff`, `lvresize -L +4G`, `mkswap` again (it is re-formatted,
so the UUID changes — update fstab if it referenced `UUID=`), `swapon`.

## 3. Btrfs and other special cases
```bash
btrfs filesystem mkswapfile --size 4g /swap/swapfile     # btrfs-progs ≥ 6.1; NOCOW, not compressed
```
Older: `truncate -s 0 f; chattr +C f; fallocate -l 4G f; chmod 0600 f`, then `mkswap f`; Btrfs swapfiles need kernel 5.0 or newer. The file must
sit on a single-device filesystem with a single data profile, in a subvolume that is **not** snapshotted (snapshots of a subvolume with
an active swapfile fail). Files made with `cp` or `truncate` have holes and are rejected by `swapon`.

## 4. zram / zswap (compressed RAM instead of, or in front of, disk)
- **zram**: a compressed block device in RAM. `zram-generator` reads its config from
  `/etc/systemd/zram-generator.conf`:
  ```
  [zram0]
  zram-size = min(ram / 2, 8192)
  compression-algorithm = zstd
  ```
  Manual: `modprobe zram`, configure a device with `zramctl` (see zramctl(8)), then `mkswap` and `swapon -p 100` it.
  Give it the highest priority so it fills before disk swap.
- **zswap**: a compressed cache *in front of* existing disk swap; `zswap.enabled=1` on
  the kernel command line. Needs real swap behind it.

## 5. Sizing and tuning
- Size swap for the workload. `vm.swappiness` (0 to 200, default 60) sets the relative IO cost of swap versus
  filesystem paging; values above 100 can suit zram or zswap (kernel vm sysctl documentation).
- Hibernation needs enough swap for the memory image **and**
  `resume=UUID=<swap uuid>` (plus `resume_offset=` for a swapfile; on Btrfs take it from
  `btrfs inspect-internal map-swapfile -r`, not from filefrag)
  on the kernel command line, then rebuild initramfs.
- Kubernetes nodes: the kubelet can run with swap when configured with `failSwapOn: false`; see the Kubernetes
  swap-memory documentation for the supported behaviour.
- Watch `vmstat 1` columns `si`/`so`: sustained swap-in/out means the host is short on
  RAM, not that swap is "bad".

## Failure modes
- `swapon: /swapfile: swapon failed: Invalid argument` — file has holes (truncate/sparse)
  or is on Btrfs with CoW/compression on.
- Boot delayed, then continues: swap entry in fstab for a device that no longer
  exists; add `nofail` or remove the line.
- System thrashes but `free` shows swap unused: `swapon --show` empty — the file was
  recreated after an update and never re-enabled.

## Verify
- [ ] `swapon --show` lists the device with the intended size and priority.
- [ ] After reboot it is still active (`free -h` Swap total > 0).
- [ ] For hibernation: `systemctl hibernate` resumes with the session intact.

## Checked

Checked 2026-10-27 against util-linux swapon(8) and mkswap(8) man page sources, btrfs-progs swapfile documentation, Linux kernel docs (zram, zswap, swsusp, vm sysctl) and the Kubernetes swap documentation, current master, 2026-10-27. Confirmed: swapon priority range and pri= fstab option, nofail option, holes and fallocate caveats and Btrfs nocow requirement, btrfs filesystem mkswapfile since 6.1 and map-swapfile -r, Btrfs single-device and snapshot limits, resume= and resume_offset= parameters, zram-generator keys, zswap.enabled, swappiness range and default, failSwapOn false. Removed or softened: ext4/XFS-only fallocate claim, the ZFS zvol advice, zramctl option list, sizing and swappiness advice, hibernation size rule, Kubernetes version gate, 90-second boot delay.

Method: documentation only; no commands were run.
