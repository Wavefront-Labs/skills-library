---
id: computing-software.systems-network-administration.windows-server.shadow-copies-for-shared-folders
name: shadow-copies-for-shared-folders
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, file-server, smb-shares, shadow-copies, previous-versions, volume-shadow-copy, diff-area, self-service-restore, ransomware]
level: practitioner
status: docs-checked
description: "Enable Shadow Copies for Shared Folders so users restore Previous Versions themselves: schedule, separate diff-area volume, storage limits, and limitations versus backups."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vssadmin
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vssadmin-resize-shadowstorage
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/shadow-copies-of-shared-folders
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shadow Copies for Shared Folders (Previous Versions)

**Goal:** users right-click a folder > Restore previous versions and recover yesterday's file
without a helpdesk ticket.

## Enable
GUI: volume Properties > Shadow Copies > select the data volume > Settings (storage area, limit, schedule) > Enable.
By default the Shadow Copies of Shared Folders feature keeps 64 shadow copies per volume; the `MaxShadowCopies`
registry key changes that limit (VSS itself allows up to 512 software shadow copies per volume).

Command line:
```cmd
vssadmin add shadowstorage /for=<DATA_DRIVE>: /on=<DIFF_DRIVE>: /maxsize=20%
vssadmin resize shadowstorage /for=<DATA_DRIVE>: /on=<DIFF_DRIVE>: /maxsize=20%
vssadmin list shadows /for=<DATA_DRIVE>:
vssadmin list shadowstorage
```
`add shadowstorage` and `create shadow` are listed in the Windows Server 2012 R2 vssadmin reference but not in the
current vssadmin reference, which lists delete shadows, the list commands and resize shadowstorage. Use the GUI to
create the association and schedule on current releases, or `diskshadow` (`create`) for a one-off snapshot.

## Sizing and placement
- The diff area can be on any local volume but must be NTFS with enough space. Microsoft recommends a separate
  physical disk for performance, and on clusters the destination drive needs a drive letter.
- When the diff area runs out of space, shadow copies for the volume are deleted beginning with the oldest; heavy
  changes to the volume consume it faster.

## Limits
- Not a backup on its own: a shadow copy is the source for a backup, and the content copied to other media is the
  backup. `vssadmin delete shadows` removes shadow copies permanently, so keep real backups and protect them.
- Users need read access to the file to restore it.

## Verify
- [ ] `vssadmin list shadows` shows snapshots at each scheduled time.
- [ ] A test user restores a deleted file via Previous Versions on the share.

## Checked

2026-10-27. Documentation release: windowsserverdocs Volume Shadow Copy Service overview, vssadmin references (current, plus the Windows Server 2012 R2 reference for add shadowstorage and create shadow) and the Support Articles page on Shadow Copies of Shared Folders on clusters. Confirmed: 64 default shadow copies for the shared-folders feature and MaxShadowCopies, 512 software shadow copy maximum, diff area location and NTFS rule, oldest-first deletion, separate-disk recommendation, delete shadows permanence, shadow copy versus backup. Removed the default schedule times, the scheduled-task name, the WMI create method, the defragmentation and deduplication warnings and the ransomware and ABE statements as unconfirmed.

Method: documentation only; no commands were run.
