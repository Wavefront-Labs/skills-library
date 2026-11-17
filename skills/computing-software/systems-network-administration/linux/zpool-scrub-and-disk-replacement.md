---
id: computing-software.systems-network-administration.linux.zpool-scrub-and-disk-replacement
name: zpool-scrub-and-disk-replacement
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, zfs, zfs-scrub, zpool-replace, resilver, zpool-status, degraded-pool, openzfs]
level: advanced
status: docs-checked
description: "Keep ZFS pools healthy: scheduled scrubs, reading zpool status errors, replacing failed or upgrading disks with zpool replace, resilver monitoring, and autoreplace/spares."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-replace.8.html
  - https://openzfs.github.io/openzfs-docs/msg/ZFS-8000-9P/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool scrub and disk replacement

## Scrub
```bash
zpool scrub tank ; zpool status tank          # progress, errors repaired
zpool scrub -p tank / -s tank                  # pause / stop
systemctl enable --now zfs-scrub-monthly@tank.timer   # unit templates shipped in the OpenZFS source tree
```
Scrub on a regular schedule. Scrubs verify every checksum and repair from redundancy.

## Read zpool status
- READ/WRITE/CKSUM counters per device: a few CKSUM errors repaired after a cable issue → `zpool clear tank` and watch;
  rising counts → replace.
- `DEGRADED`, `FAULTED`, `UNAVAIL` states; `errors: Permanent errors have been detected in the following files` = data lost
  (restore those files from backup).
- Messages reference ZFS-8000-xx codes with documented actions.

## Replace a disk
```bash
ls -l /dev/disk/by-id/ | grep -v part        # use by-id names, never sdX
zpool offline tank ata-OLD_SERIAL            # if still present
# swap hardware
zpool replace tank ata-OLD_SERIAL /dev/disk/by-id/ata-NEW_SERIAL
zpool status tank                            # 'resilver in progress', ETA
```
Same slot/same path replacement: `zpool replace tank ata-OLD_SERIAL` (new disk at the same name).
Upgrading capacity: replace each disk one at a time, then `zpool set autoexpand=on tank` (or `zpool online -e`).

## Spares and autoreplace
`zpool add tank spare /dev/disk/by-id/...`; `zpool set autoreplace=on tank` uses a new disk in the same
physical slot automatically (needs zed, the ZFS event daemon — also sends email: ZED_EMAIL_ADDR in zed.rc).

## Gotchas
- 4K disks: pool `ashift` is fixed at vdev creation — replacing with mismatched sector sizes can fail or be slow.
- Resilvering RAIDZ with large disks takes many hours; a further failure beyond the vdev's redundancy during it loses the pool.

## Verify
- [ ] `zpool status -x` reports no pools with errors; last scrub date recent with 0 errors.

## Checked

Checked 2026-10-27 against OpenZFS zpool-scrub(8), zpool-replace(8), zpool-status(8), zpool-online(8), zpoolprops(7), zed(8) man page sources, zed.rc and systemd unit templates in openzfs/zfs master, 2026-10-27. Confirmed: scrub start/pause (-p)/stop (-s), zfs-scrub-monthly@ and weekly timer templates, zpool replace and same-path replacement, autoexpand and zpool online -e, autoreplace property, zpool status -x meaning, ZED_EMAIL_ADDR in zed.rc, ashift option on replace. Removed or softened: OpenZFS 2.1 version gate, Debian cron remark, monthly/quarterly cadence advice, exact healthy-pool message.

Method: documentation only; no commands were run.
