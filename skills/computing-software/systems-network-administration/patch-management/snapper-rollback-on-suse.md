---
id: computing-software.systems-network-administration.patch-management.snapper-rollback-on-suse
name: snapper-rollback-on-suse
category: computing-software
field: systems-network-administration
product: patch-management
tags: [snapper-rollback, snapper, btrfs, opensuse, sles, linux-patch-tooling]
level: practitioner
status: docs-checked
description: "Use Btrfs snapper pre/post snapshots on SLES/openSUSE to roll back failed updates: zypper snapshot pairs, booting a snapshot from GRUB, snapper rollback and cleanup."
sources:
  - https://documentation.suse.com/sles/15-SP6/html/SLES-all/cha-snapper.html
  - https://documentation.suse.com/sle-micro/6.0/html/Micro-transactional-updates/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Btrfs snapper rollback on SUSE

SLES and openSUSE with a Btrfs root create snapshots automatically before and after each zypper transaction (snapper zypp plugin). A bad update can be undone in minutes.

## See snapshots
```sh
snapper list                   # zypper pairs are Pre & Post snapshots described as zypp(zypper)
snapper status 41..42          # files changed by the update (numbers are examples)
snapper diff 41..42 /etc/ssh/sshd_config
```

## Undo file changes only (system still running)
`snapper undochange 41..42` reverts files changed between 41 and 42. Not suitable for kernel or running library changes.

## Full rollback
1. If the system boots: `snapper rollback <number>` (or plain `snapper rollback`) creates a backup snapshot of the current state and a new read-write default snapshot; reboot afterwards.
2. If it does not boot: in GRUB choose **Start bootloader from a read-only snapshot**, pick the pre snapshot, boot it, test, then run `snapper rollback` (no number needed when booted from the snapshot) and reboot.

## What is not rolled back
The SLES documentation lists these as excluded from root snapshots: the architecture-specific `/boot/grub2` directories (a boot loader rollback is not supported), `/home` when it is not on a separate partition, `/opt`, `/srv`, `/tmp`, `/usr/local`, and `/var` (logs, caches, `/var/opt`, virtual machine images and databases). Restore data in those locations separately.

## Cleanup
Settings in `/etc/snapper/configs/root`: `NUMBER_CLEANUP`, `NUMBER_LIMIT` (SLES 15 SP6 default 2-10) and `NUMBER_LIMIT_IMPORTANT` (default 4-10); `TIMELINE_CREATE` switches timeline snapshots on or off. Full Btrfs filesystems break updates: check `btrfs filesystem usage /` and delete old snapshots with `snapper delete`.

## Transactional systems
SLE Micro / openSUSE MicroOS: `transactional-update` writes updates into a new snapshot, active after reboot; `transactional-update rollback [<n>|last]` sets a working snapshot as the default, followed by a reboot.

## Gotchas
- Rolling back leaves the newer snapshot; the next zypper run will reinstall the update unless you lock it (`zypper al <pkg>`).
- Root filesystem on ext4/XFS = no snapper rollback.

## Verify
`snapper list` shows the rollback backup snapshot and the new default, `rpm -q` shows previous versions, and the problem package is locked until fixed.

## Checked

Checked 2026-10-27 against the SLES 15 SP6 snapper chapter and the SLE Micro transactional-update guide (6.0).
- Pre & Post pairs labelled zypp(zypper), `snapper status/diff/undochange PRE..POST`: confirmed.
- `snapper rollback` from a running system and from a snapshot booted via "Start bootloader from a read-only snapshot", reboot afterwards, backup snapshot created: confirmed.
- Excluded directories list; `NUMBER_LIMIT` 2-10 and `NUMBER_LIMIT_IMPORTANT` 4-10 defaults: confirmed. `/root` is not in the documented list and was removed.
- `transactional-update rollback [number|last]`: confirmed.
Method: documentation only; no commands were run.
