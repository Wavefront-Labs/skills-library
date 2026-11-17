---
id: computing-software.it-support-helpdesk.desktop-support.system-image-backup-and-restore-testing
name: system-image-backup-and-restore-testing
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, system-image-backup, restore-test-procedure, endpoint-backup-agent, backup-restore, bare-metal-restore]
level: practitioner
status: draft
description: "Take and restore system image backups, test restores on a schedule with documented results, and troubleshoot endpoint backup agents that stop backing up."
sources:
  - "https://support.microsoft.com/en-us/windows/back-up-and-restore-in-windows-352091d2-bb9d-3ea3-ed18-52ef2b88cbef"
  - "https://www.cisa.gov/stopransomware/ransomware-guide"
  - "https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# system-image-backup-and-restore-testing

## System image backups
- Windows built-in "Backup and Restore (Windows 7)" can still create a system image
  (`sdclt` > Create a system image) and `wbadmin start backup -backupTarget:E:
  -include:C: -allCritical -quiet`. Deprecated but present; fine for one-off images.
- Commercial endpoint/backup tools (Veeam Agent, Acronis, Macrium) do image-based
  backups with incremental chains and bare-metal recovery media.
- Corporate endpoints usually don't need images: OneDrive/KFM for data and
  Autopilot/reimage for the OS is faster. Images make sense for special-purpose PCs
  (lab instruments, legacy software that can't be reinstalled).
- Restore: boot recovery media (WinRE "System Image Recovery" for wbadmin images, or
  vendor media), choose the image; target disk same size or larger.

## Restore testing
Backups that were never restored are hopes. Schedule tests:
| What | How often | Test |
|---|---|---|
| File restore from endpoint backup / OneDrive | Monthly | Restore a random file to an alternate location, open it |
| Full image of a special PC | Quarterly | Restore to spare hardware or VM, boot, run the app |
| M365 restore (mailbox item, SharePoint) | Quarterly | Restore per runbook |
Record: date, what was restored, time taken, success, issues. Time taken tells you
real RTO.

## Endpoint backup agent troubleshooting
- Last successful backup old: check agent service running, device online during the
  backup window (laptops asleep at 2 am never back up; use "back up when online" or
  run at login), disk space for local cache, credentials/token expired.
- VSS errors: `vssadmin list writers` (writers in failed state), `vssadmin list
  shadowstorage`; restart the related service (e.g. SQL Writer) or reboot; event log
  VSS errors 8193/12289.
- Excluded data: check include/exclude policy covers the user's actual folders.
- Throttling or VPN-only backups never completing: allow backups direct to cloud.
- Use RMM/backup console alerting so failures become tickets.

## Verify
The latest restore test succeeded and is logged, and every in-scope endpoint shows a
successful backup within the policy window.
