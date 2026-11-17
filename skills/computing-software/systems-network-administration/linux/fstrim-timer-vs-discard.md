---
id: computing-software.systems-network-administration.linux.fstrim-timer-vs-discard
name: fstrim-timer-vs-discard
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fstrim, discard, ssd-trim, fstrim-timer, thin-provisioning, lvm-issue-discards, luks-discard]
level: practitioner
status: docs-checked
description: "Keep SSDs and thin storage reclaimed: periodic fstrim.timer vs the discard mount option, passing TRIM through LUKS/LVM/VMs, and checking support with lsblk --discard."
sources:
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/fstrim.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/fstrim.timer
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/fstrim.service.in
  - https://github.com/util-linux/util-linux/blob/master/lsblk-cmd/lsblk.8.adoc
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-mount-options.rst
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/common_options.adoc
  - https://github.com/lvmteam/lvm2/blob/master/conf/example.conf.in
  - https://github.com/libvirt/libvirt/blob/master/docs/formatdomain.rst
  - https://github.com/systemd/systemd/blob/main/man/crypttab.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fstrim vs discard

## Check support through the whole stack
```bash
lsblk --discard          # DISC-GRAN / DISC-MAX non-zero = device (and each layer) passes discards
```
Zeros on a layer (LUKS, dm, virtual disk) mean TRIM stops there.

## Periodic TRIM (recommended)
```bash
systemctl enable --now fstrim.timer      # weekly, trims all mounted filesystems that support it
fstrim -av                               # manual, verbose: prints '/: <size> (<n> bytes) trimmed'
```
## Continuous discard
Mount option `discard` (ext4/XFS) or `discard=async` (Btrfs: async is the default when the device supports it, since 6.2). The fstrim man page warns
that frequent trimming or `mount -o discard` can shorten the life of poor-quality SSDs and that trim commands cost performance;
once a week is usually sufficient, so periodic is the safer default. Using both is redundant.

## Layers
- LUKS: `discard` in `/etc/crypttab` options (or `cryptsetup --allow-discards`, LUKS2 can persist with
  `cryptsetup refresh --persistent --allow-discards`). cryptsetup warns that it can reveal filesystem type and used space.
- LVM: fstrim on the LV works with thin pools; `issue_discards = 1` in lvm.conf only affects lvremove/lvreduce.
- VMs: libvirt's `discard='unmap'` on the disk `<driver>` element passes guest discard requests on (value `ignore` drops them).

## Gotchas
- `fstrim: /: the discard operation is not supported` — a layer blocks it (see lsblk --discard).

## Verify
- [ ] `systemctl list-timers fstrim.timer` shows NEXT; `fstrim -av` trims; thin pool usage (`lvs` Data%) drops after deletes.

## Checked
Checked 2026-10-26 against util-linux master (fstrim man page source, fstrim.timer, fstrim.service.in, fstrim.c, lsblk source), btrfs-progs mount options, cryptsetup man page sources, lvm2 example.conf, libvirt formatdomain and systemd crypttab.
Confirmed: the weekly fstrim.timer and the `--listed-in /etc/fstab:/proc/self/mountinfo` service; `fstrim -a -v` output format; the man-page warning about frequent trimming and `mount -o discard`; the "discard operation is not supported" message; `lsblk --discard` columns DISC-GRAN and DISC-MAX; Btrfs `discard=async` default since 6.2; crypttab `discard`; cryptsetup `--allow-discards` and `refresh --persistent`; lvm.conf `issue_discards` acting on lvremove and lvreduce; libvirt `discard='unmap'`.
Removed as unconfirmed: the md RAID5/6 module parameter, the old-SATA blacklist remark and cloud provider claims.
Method: documentation only; no commands were run.
