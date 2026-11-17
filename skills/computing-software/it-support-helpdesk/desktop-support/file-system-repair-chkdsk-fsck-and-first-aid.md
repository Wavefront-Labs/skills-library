---
id: computing-software.it-support-helpdesk.desktop-support.file-system-repair-chkdsk-fsck-and-first-aid
name: file-system-repair-chkdsk-fsck-and-first-aid
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, chkdsk-repair, file-system-corruption, fsck, disk-utility-first-aid, ntfs, apfs]
level: practitioner
status: draft
description: "Repair file system corruption across platforms: chkdsk on NTFS, fsck on Linux, Disk Utility First Aid and fsck_apfs on macOS, with backup-first rules and log reading."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chkdsk"
  - "https://support.apple.com/guide/disk-utility/repair-a-storage-device-dskutl1040/mac"
  - "https://man7.org/linux/man-pages/man8/fsck.8.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# file-system-repair-chkdsk-fsck-and-first-aid

## Signs of file system corruption
Files or folders that can't be opened or deleted ("file or directory is corrupted and
unreadable"), wrong free space, event ID 55/98 (Ntfs) in the System log, apps failing
on specific files, macOS "disk wasn't repaired completely".

## Rule 1: is the drive failing?
Check SMART/drive health first. Running repairs on a dying drive can finish it off;
image or copy data first, then repair.

## Windows: chkdsk
```
chkdsk C:                 & rem read-only scan
chkdsk C: /scan           & rem online scan (NTFS), no downtime
chkdsk C: /spotfix        & rem fix issues found by /scan, brief offline
chkdsk C: /f              & rem fix errors (system volume: schedules at next boot)
chkdsk D: /r              & rem /f plus locate bad sectors (slow, hours on big HDDs)
fsutil dirty query C:     & rem is the volume flagged dirty
```
- Results of boot-time chkdsk: Event Viewer > Application log, source **Wininit**
  (event 1001).
- On SSDs avoid routine `/r`; it adds wear for little value.
- ReFS volumes don't use chkdsk.

## Linux: fsck
- Never run on a mounted read-write file system. Boot to rescue/live media or unmount:
```
sudo umount /dev/sdb1
sudo fsck -f /dev/sdb1          # ext4: -y to auto-answer yes
sudo xfs_repair /dev/sdb1       # XFS uses xfs_repair, not fsck
```
- Root file system: `sudo touch /forcefsck` (older) or add `fsck.mode=force` to the
  kernel command line for one boot; systemd-fsck runs at boot per `/etc/fstab` pass
  field.

## macOS: First Aid
- Disk Utility > View > Show All Devices; run First Aid on the **volume**, then the
  container, then the physical disk.
- Startup disk: First Aid in Recovery (Apple silicon: hold power > Options).
- Command line: `diskutil verifyVolume /`, `diskutil repairVolume disk3s5`;
  `fsck_apfs -n /dev/disk3s5` for read-only check.
- "First Aid process has failed" repeatedly: back up and erase/reinstall, check the
  drive.

## After repair
- Check what chkdsk/fsck moved: `found.000` folders (Windows) or `lost+found` (Linux)
  hold recovered fragments.
- Find the cause: unexpected power loss, failing disk, faulty cable/enclosure, bad RAM.

## Verify
A follow-up read-only scan reports no errors, the affected files open (or are restored
from backup), and the root cause has been noted.
