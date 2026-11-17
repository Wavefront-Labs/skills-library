---
id: computing-software.systems-network-administration.backup-and-recovery.zfs-snapshot-holds-and-pull-replication
name: zfs-snapshot-holds-and-pull-replication
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [zfs-hold, pull-replication, zfs-send, syncoid, sanoid, immutable-snapshots]
level: advanced
status: docs-checked
description: "Protect ZFS backups with snapshot holds and pull-based replication: zfs hold/release, a backup server that pulls with a restricted key, and limits of these protections."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-hold.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
  - https://github.com/jimsalterjrs/sanoid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZFS snapshot holds and pull replication

## Snapshot holds
A hold makes `zfs destroy` of a snapshot fail with `EBUSY` until all holds are released. Each snapshot has its own tag namespace and `-r` applies a hold recursively to descendant snapshots.
```
zfs hold keep pool/data@2026-10-18     # add a tag
zfs holds pool/data@2026-10-18         # list
zfs release keep pool/data@2026-10-18  # remove
```
- Protects against accidental or scripted deletion and pruning tools.
- Root can still release holds; a hold is not immutability against an attacker with root on that host.

## Pull replication
The backup host initiates the connection and pulls snapshots, so a compromised source host has no credentials to the backup host.
- On the source, create a restricted user and delegate only send rights:
  `zfs allow -u backup send,hold,release pool/data`
  (`send`, `hold`, `release` and `snapshot` are delegable subcommand permissions; `snapshot` also needs `mount`.)
- On the backup host, pull with syncoid:
  `syncoid --no-privilege-elevation --sendoptions=w backup@src:pool/data backuppool/src/data`
  (`--no-privilege-elevation` skips syncoid's root check for use with permission delegation; `w` in `--sendoptions` is `zfs send -w`, a raw send that keeps encrypted datasets encrypted.)
- On the backup host, prune with its own sanoid policy (keep longer than the source).
- Limit what the pulling SSH key can run on the source.

## Hardening the backup host
- No inbound SSH from production; admin via a separate network and MFA.
- Don't mount received datasets read-write (`zfs set readonly=on backuppool/src`).
- Optionally hold the latest N snapshots automatically after each pull so a mistaken prune cannot remove them.

## Gotchas
- An incremental send needs a common snapshot on both sides; pruning the last common one forces a full resend. Syncoid's `--use-hold` places a hold on the newest replicated snapshot on source and target, and `--create-bookmark` (with `--no-sync-snap`) keeps a bookmark so replication can continue if the last common snapshot is deleted.
- Raw sends of encrypted data need keys only at restore time; store keys separately.

## Verify
On the source, `zfs destroy` of a held snapshot fails; from the source host, attempting to SSH into the backup host fails; a test restore with `zfs send | zfs recv` from backup completes.

## Checked

Checked 2026-10-27 against the OpenZFS man pages in openzfs/zfs (zfs-hold 8, zfs-allow 8, zfs-send 8) and the Sanoid README and syncoid script in jimsalterjrs/sanoid. Confirmed: `zfs hold`, `zfs holds`, `zfs release` syntax and the EBUSY result on destroy, the delegable `send`, `hold`, `release` and `snapshot` permissions, the `-w` raw send option, and the syncoid options `--no-privilege-elevation`, `--sendoptions` (accepting `w`), `--use-hold` and `--create-bookmark`.

Method: documentation only; no commands were run.
