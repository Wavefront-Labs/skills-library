---
id: computing-software.systems-network-administration.linux.vdo-dedup-compression-volumes
name: vdo-dedup-compression-volumes
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vdo, vdo-volume, vdo-dedup, lvm-vdo, deduplication, compression, thin-provisioning, vdostats, rhcsa, rhel, sysadmin]
level: practitioner
status: docs-checked
description: "Create and run LVM-VDO volumes on RHEL 9 for deduplication and compression: sizing physical vs virtual space, mkfs options, monitoring savings, and avoiding out-of-space."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmvdo.7_main
  - https://github.com/lvmteam/lvm2/blob/main/lib/report/columns.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VDO (LVM-VDO) deduplication and compression

**Goal:** store VM images, backups or container layers in less physical space, without
running out of real space while the filesystem thinks it has plenty.

## 1. Concepts
VDO is a device-mapper layer doing inline zero-block elimination, deduplication (UDS index)
and compression. Physical size = real disk; **virtual (logical) size** = what the filesystem
sees. Without an explicit virtual size, lvm creates the VDO LV with the maximum size that fits even if the data is incompressible.
VDO is managed through LVM (`--type vdo`); `lvm_import_vdo` converts volumes created with the older standalone vdo tool.
Only a single VDO LV per VDO pool is currently supported.

## 2. Create
```bash
vgcreate vg_vdo /dev/sdb
lvcreate --type vdo -n vdo1 -L 500G -V 2T vg_vdo     # 500G physical data size, 2T virtual LV (pool named vpool0, vpool1, ...)
mkfs.ext4 -E nodiscard /dev/vg_vdo/vdo1               # skip discards at mkfs: TRIM on large VDO volumes is slow
```
TRIM/discard on large VDO volumes is slow, so lvmvdo(7) advises avoiding discard requests unless necessary.
Options at create: `--compression y|n`, `--deduplication y|n`, `--vdosettings 'vdo_slab_size_mb=…'` (explicit `--compression` and `--deduplication` have the highest priority). Change later with `lvchange --compression` / `--deduplication`.

## 3. Monitor
```bash
lvs -a -o name,size,data_percent,vdo_saving_percent,vdo_compression_state vg_vdo   # Data% = virtual data used and space consumed in the pool
vdostats --all /dev/mapper/vg_vdo-vpool0-vpool    # detailed statistics (vdostats understands only /dev/mapper names)
```
**Watch the pool's physical usage** (lvs Data% on the pool, vdostats), not `df`: the virtual size can promise more than the physical data size holds. Grow physical: `lvextend -L +200G vg_vdo/vpool0` (adds at least one slab; a pool cannot be reduced), or set `vdo_pool_autoextend_threshold`/`vdo_pool_autoextend_percent` for a monitored pool; grow virtual: `lvextend -L +1T vg_vdo/vdo1` then grow the fs. Reducing the virtual size needs TRIM of the freed area, which can take long.

## 4. Fit
Measure the saving on representative data (`vdo_saving_percent`) before committing to a virtual size.

## Gotchas
- VDO uses RAM for its deduplication index (`vdo_index_memory_size_mb`, default 256 in lvmvdo(7); `vdo_use_sparse_index` defaults to 0) — size hosts accordingly.
- Discards are slow on large VDO volumes but free the unmapped blocks; use them deliberately (for example a scheduled `fstrim`).

## Verify
- [ ] `vdo_saving_percent` is above 0 after loading representative data.
- [ ] Monitoring alerts on physical usage, not filesystem usage.
- [ ] After a deliberate `fstrim -v /mount`, pool usage drops.

## Checked

Checked against the lvm2 main branch man/lvmvdo.7_main and lib/report/columns.h (repository last pushed 2026-10-09).
Confirmed: `lvcreate --type vdo -n -L -V`; pool naming vpool0, vpool1; `lvchange --compression/--deduplication`; `--vdosettings` keys and defaults shown; `lvm_import_vdo`; pool extension rules and autoextend settings; discard slowness and `mkfs.ext4 -E nodiscard`; the lvs fields `vdo_saving_percent` and `vdo_compression_state`; `vdostats --all` with /dev/mapper names.
Removed unconfirmed claims: RHEL package names, `mkfs.xfs -K`, the `defaults,discard` fstab recommendation (the man page advises avoiding discards), savings multipliers, the 1 GB per TB index sizing, the 80 percent alert level, the LUKS ordering advice, write-speed remarks and `vdostats --human-readable`/`--verbose`.

Method: documentation only; no commands were run.
