---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-disk-volumes-and-vchanger
name: bacula-disk-volumes-and-vchanger
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula, bacula-disk, vchanger, virtual-autochanger, file-device, bareos]
level: practitioner
status: docs-checked
description: "Run Bacula on disk: file devices, virtual disk autochangers with multiple devices, volume size and job limits, automatic labelling, and vchanger for rotating removable disks."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Automated_Disk_Backup.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Storage_Daemon_Configuratio.html
  - https://sourceforge.net/projects/vchanger/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula disk volumes and virtual autochangers

**Goal:** disk-based Bacula that runs jobs concurrently, recycles space predictably, and can rotate removable disks offsite.

## Virtual disk autochanger (bacula-sd.conf)
```
Autochanger {
  Name = FileChgr1
  Device = FileChgr1-Dev1, FileChgr1-Dev2, FileChgr1-Dev3
  Changer Command = ""
  Changer Device = /dev/null
}
Device {
  Name = FileChgr1-Dev1
  Media Type = File1
  Archive Device = /srv/bacula/volumes
  LabelMedia = yes; Random Access = yes; AutomaticMount = yes
  RemovableMedia = no; AlwaysOpen = no
  Maximum Concurrent Jobs = 5
  Autochanger = yes
}
```
`Random Access = yes` is for file systems (all file devices must be random access). `Maximum Concurrent Jobs` on a Device caps jobs on that one device, so several devices let jobs use more than one at a time.

## Pool settings for disk
```
Pool {
  Name = Disk-Incr
  Label Format = "Incr-"
  Maximum Volume Bytes = 50G
  Maximum Volume Jobs = 1          # or a size cap
  Volume Retention = 30 days
  AutoPrune = yes; Recycle = yes
  Action On Purge = Truncate
}
```
`Action On Purge = Truncate` only permits truncation: the volume is not truncated when purged. Set it in the Pool, run `update volumes` so existing volumes pick it up, and after the volume is purged use the console `truncate` command to free the disk space.

## vchanger (removable disks)
vchanger is a separate (third-party) tool that emulates a magazine-based tape autoloader using disk partitions on fixed or removable drives as virtual magazines, and files on them as virtual tape volumes. Follow its own documentation for the `Changer Command` line and magazine setup, then run `update slots` in bconsole after swapping disks.

## Gotchas
- Each Device needs a unique `Media Type`, because Bacula uses it to choose the device (including at restore). Give each storage location its own.

## Verify
`list volumes pool=Disk-Incr` shows volumes cycling through Purged and Recycle, and disk usage is flat over a retention cycle.

## Checked
2026-10-28. Confirmed against the Bacula 15.0.x manual pages Automated Disk Backup, Storage Daemon Configuration (`Autochanger`, `Changer Command`, `Changer Device`, `Random Access`, `Media Type`, `Maximum Concurrent Jobs`), Configuring the Director (`Action On Purge`, `Maximum Volume Jobs`) and the vchanger project page. Removed: the exact vchanger `Changer Command` string, the VirtualFull and copy-job claim, the "one giant volume" and free-space-monitoring gotchas, and `update slots` as a command syntax guarantee beyond the bconsole name.
Method: documentation only; no commands were run.
