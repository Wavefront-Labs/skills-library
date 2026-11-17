---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.raid-degraded-array-handling
name: raid-degraded-array-handling
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, storage-troubleshooting, raid-degraded, raid-rebuild, raid-levels, hot-spare, storage-spaces, nas, mdadm, perccli, comptia-a-plus, raid-level-selection]
level: practitioner
status: draft
description: "Respond to a degraded RAID or NAS volume: confirm the failed disk, back up first, replace the right drive, monitor the rebuild, and RAID level tolerances."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://raid.wiki.kernel.org/index.php/Linux_Raid"
  - "https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-states"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raid-degraded-array-handling

Goal: get a degraded array back to redundant without turning one failed
disk into total data loss.

## RAID levels — what one more failure does
| Level | Min disks | Survives | Degraded risk |
|---|---|---|---|
| 0 | 2 | nothing | n/a — any failure = data loss |
| 1 | 2 | 1 disk | no redundancy until rebuild |
| 5 | 3 | 1 disk | second failure during rebuild = loss; rebuild stresses all disks |
| 6 | 4 | 2 disks | safer for large drives |
| 10 | 4 | 1 per mirror pair | fast rebuild |
RAID is not backup.

## Procedure
1. **Confirm** which disk failed and the array state: controller utility
   (Dell `perccli /c0 show`, HPE `ssacli ctrl all show config`), NAS web UI
   (Synology Storage Manager, QNAP Storage & Snapshots), Linux
   `cat /proc/mdstat` / `mdadm --detail /dev/md0`, Windows Storage Spaces
   `Get-StoragePool`, `Get-PhysicalDisk`.
2. **Back up now** — verify a recent good backup exists before touching
   anything; rebuilds are when second disks die.
3. **Identify physically**: blink the drive LED (`perccli /c0/e32/s4 start
   locate`, NAS "locate"), match serial number. Pulling the wrong drive in
   RAID 5 = array offline.
4. Replace with same or larger capacity, same type (SAS/SATA, ideally same
   model family); not SMR drives in RAID if avoidable.
5. Rebuild starts automatically (or with a hot spare already did) — or add
   manually: `mdadm --add /dev/md0 /dev/sdd1`.
6. **Monitor**: rebuild hours to a day+ on large drives; reduce load if
   possible; watch other disks' SMART.

## Gotchas
- Multiple disks from the same batch fail close together — check SMART on
  all members during degradation.
- "Foreign configuration" on an inserted drive: clear it only after
  confirming it's the new disk, not an array member from elsewhere.
- Consumer NAS with RAID 5 on large disks + unreadable sector during rebuild
  (URE) = failed rebuild; RAID 6/SHR-2 recommended.
- Don't initialise or "create new array" over a failed one to make errors
  go away.

## Verify
Array state Optimal/Healthy/clean, all members online, email alerts
configured so the next failure is seen the same day.
