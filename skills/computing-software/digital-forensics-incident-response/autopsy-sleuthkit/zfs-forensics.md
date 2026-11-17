---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.zfs-forensics
name: zfs-forensics
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [zfs-forensics, zfs, openzfs, snapshots, truenas, dfir]
level: advanced
status: draft
description: "Examine ZFS pools forensically: read-only import of images, snapshots and zpool history, dataset properties, deleted data via older transaction groups, and tool limits."
sources: ["https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html", "https://openzfs.github.io/openzfs-docs/man/master/8/zpool-history.8.html", "https://openzfs.github.io/openzfs-docs/man/master/8/zdb.8.html", "https://dfrws.org/presentation/forensic-analysis-of-the-zfs-file-system/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ZFS forensics

ZFS (TrueNAS, Proxmox, FreeBSD, Solaris, Ubuntu root-on-ZFS) is copy-on-write with built-in volume management, so The Sleuth Kit and Autopsy cannot parse it. Work with OpenZFS tools on a Linux/FreeBSD forensic host against images, read-only.

## Mounting images safely
1. Image every member disk of the pool (mirror/RAIDZ vdevs need all or enough members).
2. Attach images read-only as loop devices: `losetup -r -f --show disk1.dd` (repeat per disk).
3. Import read-only without mounting, under an alternate root, and without changing the pool's host ID:
```bash
zpool import -d /dev/loop -o readonly=on -N -R /mnt/case <poolname>
zfs list -t all -o name,used,creation,mountpoint
zfs mount -a   # mounts under /mnt/case, read-only because the pool is
```
`-f` may be needed if the pool was not exported; with `readonly=on` nothing is written.

## High-value artefacts
- **`zpool history -il <pool>`**: every administrative command with timestamp, user and host (`zfs destroy`, `zfs rollback`, `zpool create`, property changes). Attackers and ransomware destroying snapshots show up here.
- **Snapshots** (`zfs list -t snapshot`): browse `/.zfs/snapshot/<name>/` in each dataset to recover earlier file versions; diff with `zfs diff pool/ds@snap1 pool/ds@snap2`.
- **Dataset properties** (`zfs get all`): encryption, compression, creation time, `com.sun:auto-snapshot`, user properties.
- **Encryption**: native encryption needs the key (`zfs load-key`); metadata like dataset names and sizes remain readable without it.

## Deleted data
Copy-on-write leaves old blocks until reused. Older uberblocks (transaction groups) may point to previous trees: `zdb -ul <device>` lists uberblocks; `zpool import -T <txg> -o readonly=on` imports a pool as of an earlier txg (rewind). This is fragile; only on copies.
`zdb -dddd pool/ds <object>` dumps object metadata for low-level analysis.

## Gotchas
- Never import a pool from evidence read-write; even a normal import updates labels and txgs.
- Pool features newer than your forensic host's OpenZFS version block import; match or exceed the source version.
- ZFS timestamps are nanosecond `crtime/mtime/ctime/atime` via `stat`; `atime` may be off (`atime=off`).

## Verify
Image hashes are unchanged after analysis, and `zpool history` output and snapshot listings are exported to the case with the tool version used.
