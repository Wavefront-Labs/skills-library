---
id: computing-software.systems-network-administration.linux.btrfs-send-receive-replication
name: btrfs-send-receive-replication
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, btrfs, btrfs-send, btrfs-receive, btrfs-snapshots, incremental-backup, subvolumes, replication, btrbk, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Back up and replicate Btrfs subvolumes with read-only snapshots and btrfs send/receive: full and incremental (-p) streams, over SSH, to files, and retention with btrbk."
sources:
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-send.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-receive.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-subvolume-intro.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-subvolume.rst
  - https://github.com/digint/btrbk/blob/master/doc/btrbk.conf.5.asciidoc
  - https://github.com/digint/btrbk/blob/master/doc/btrbk.1.asciidoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# btrfs send/receive

**Goal:** efficient incremental backups of Btrfs subvolumes to another disk or host — only
changed extents travel, and the target is a browsable snapshot.

## 1. Full send
```bash
btrfs subvolume snapshot -r /data /data/.snapshots/data-2026-10-16      # must be read-only
sync
btrfs send /data/.snapshots/data-2026-10-16 | btrfs receive /mnt/backup/
btrfs send /data/.snapshots/data-2026-10-16 | ssh backup01 'btrfs receive /backup/web01/'
btrfs send -f data-full.stream /data/.snapshots/data-2026-10-16          # to a file (any fs/tape)
btrfs receive -f data-full.stream /mnt/backup/
```
Target must be a Btrfs filesystem (for receive); stream files can live anywhere.

## 2. Incremental
```bash
btrfs subvolume snapshot -r /data /data/.snapshots/data-2026-10-17
btrfs send -p /data/.snapshots/data-2026-10-16 /data/.snapshots/data-2026-10-17 \
  | ssh backup01 'btrfs receive /backup/web01/'
```
The parent (`-p`) snapshot must exist **unchanged on both sides** — keep at least the most
recent common snapshot on source and target. `-c` clone sources allow sharing extents with
other snapshots present on both sides.

## 3. Restore
Send back the other way (`btrfs send /backup/web01/data-2026-10-17 | btrfs receive /restore/`),
then `btrfs subvolume snapshot /restore/data-2026-10-17 /data` to get a writable copy (received
subvolumes are read-only). `btrfs property set -f -t subvol <subvol> ro false` makes it writable in place; force is
required for a received subvolume because it resets `received_uuid`, which can break incremental send.

## 4. Automate retention: btrbk
```
# /etc/btrbk/btrbk.conf
snapshot_preserve_min   2d
snapshot_preserve       14d
target_preserve_min     no
target_preserve         20d 10w *m
volume /mnt/btr_pool
  snapshot_dir btrbk_snapshots
  subvolume data
    target ssh://backup01/backup/web01
```
Run `btrbk dryrun` first, then `btrbk run` (for example from a daily timer); `btrbk list backups`.
`snapshot_preserve` and `target_preserve` have no effect while the matching `_min` option is `all`
(the default), and `*m` keeps all monthly backups. btrbk does not create the `snapshot_dir`; create it first.

## Gotchas
- All snapshots in a send must be read-only; sending a writable subvolume fails.
- Lost common parent → next send must be full; never delete the last common snapshot on either side.
- Making a received subvolume read-write requires resetting its `received_uuid`, which can break incremental send; `btrfs receive` also fails if a previously received subvolume was changed after it was received.
- Snapshots aren't backups until they're on another device.

## Verify
- [ ] `btrfs subvolume list -R /backup/web01` shows received snapshots with received_uuid.
- [ ] Incremental send is much smaller than full (`btrfs send … | wc -c` or `pv`).
- [ ] A restore test of a file from the target matches the source.

## Checked
Checked 2026-10-26 against btrfs-progs Documentation (master, pushed 2026-10-23: btrfs-send, btrfs-receive, btrfs-subvolume, ch-subvolume-intro, btrfs-property) and the btrbk man page sources (digint/btrbk master).
Confirmed: send needs read-only snapshots; `-p`, `-c`, `-f`; parent and clone sources must be identical on both sides; received subvolumes are read-only and snapshots default to read-write; `btrfs subvolume list -R`; btrbk keys `volume`, `subvolume`, `snapshot_dir`, `target ssh://...`, `*` for all monthly backups, and the commands `run`, `dryrun`, `list backups`.
Wrong in the draft: the property command lacked `-f` (forcing is required for received subvolumes) and used `-ts`; the btrbk example had no `target_preserve_min`, so `target_preserve` would have had no effect (the default `all` disables it).
Removed as unconfirmed: the snap-sync remark and the exact "not read-only" error text.
Method: documentation only; no commands were run.
