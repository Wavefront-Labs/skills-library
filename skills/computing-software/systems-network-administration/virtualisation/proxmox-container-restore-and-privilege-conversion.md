---
id: computing-software.systems-network-administration.virtualisation.proxmox-container-restore-and-privilege-conversion
name: proxmox-container-restore-and-privilege-conversion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pct-restore, lxc, proxmox, backup-restore]
level: practitioner
status: docs-checked
description: "Restore Proxmox VE containers from vzdump or PBS with pct restore, convert privileged containers to unprivileged, resize rootfs and handle mount points."
sources:
  - https://pve.proxmox.com/pve-docs/pct.1.html
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#vzdump_restore
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container restore and privilege conversion

**Goal:** bring a container back from backup, optionally changing storage, size or privilege mode.

## Restore
```bash
pct restore 120 /mnt/backup/dump/vzdump-lxc-120-2026_10_01-02_00_00.tar.zst --storage local-lvm
pct restore 120 pbs-store1:backup/ct/120/<backup-time> --storage ceph-rbd            # from PBS
pct restore 121 <archive> --storage local-lvm --rootfs local-lvm:16                  # new ID and bigger rootfs
pct restore 120 <archive> --force                                                     # overwrite existing CT 120
```
GUI: storage -> Backups -> Restore, or the CT's Backup tab.

## Privileged to unprivileged
```bash
pct restore 130 <archive-of-privileged-ct> --storage local-lvm --unprivileged 1
```
The unprivileged container maps root inside to an unprivileged user outside, so extraction runs with the shifted ownership. Use `--ignore-unpack-errors 1` if extraction stops on errors (for example device nodes), then check services that relied on them..

## Mount points
Only mount points with `backup=1` are in the archive. Simple restore recreates storage-backed mount points and adds bind and device mount points back as configuration only (limited to root); their content is never backed up. Setting `--rootfs` and/or `--mpX` switches to advanced restore, which ignores the rootfs and mpX entries in the archive and uses only the parameters you give.

## Gotchas
- Restoring to a different storage type changes snapshot capability; check what the target storage supports.
- `--force` allows overwriting an existing container; without it, restoring onto an existing ID is refused.
- Unprivileged conversion with bind mounts needs idmap or host ownership changes.

## Verify
`pct config 130` shows `unprivileged: 1` and the expected rootfs; `pct start 130 && pct enter 130` and services run.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc Backup and Restore; generated pct.1-synopsis.adoc pct restore options) and confirmed the pct restore options --storage, --rootfs, --unprivileged, --force and --ignore-unpack-errors, plus the simple versus advanced restore behaviour for mount points. Removed the unconfirmed uid 100000 figure and the volume-destruction claim.

Method: documentation only; no commands were run.
