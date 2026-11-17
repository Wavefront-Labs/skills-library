---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-powershell-module
name: veeam-powershell-module
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-powershell, veeam, veeam-backup-and-replication, automation, backup-reporting, veeam-backup-job]
level: practitioner
status: docs-checked
description: "Veeam Backup PowerShell module: where it installs, required role, PowerShell 5.1 and MFA limits, and how to start a session locally or remotely."
sources:
  - https://helpcenter.veeam.com/docs/backup/powershell/getting_started.html?ver=120
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam PowerShell module

The Veeam Backup PowerShell module is added to a machine when you install the Veeam Backup & Replication server or the Veeam Backup & Replication Console. It can do almost all operations available in the UI, with the same force: deleting a job with a script removes it from the configuration database and cannot be undone.

## Requirements and limits
- You need the Veeam Backup Administrator role.
- Windows PowerShell 5.1 on the machine running the session.
- MFA is not supported for PowerShell (interactive or non-interactive). Run the console or PowerShell under a service account with MFA disabled.
- Veeam Support does not write scripts on demand and does not troubleshoot custom scripts. The PowerShell Reference does not document internal .NET classes and methods.

## Starting a session
- On the backup server: in the main menu choose **Console > PowerShell**, or start the Windows PowerShell console directly.
- From a remote machine: install the Veeam Backup & Replication Console there (it installs the module by default), then run the cmdlets from it.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Getting Started" (PowerShell reference, v12.0 archive copy, read in part).
Removed (cmdlet reference pages were not read, so none could be confirmed): all example code (`Connect-VBRServer`, `Get-VBRJob`, `Find-VBRViEntity`, `Start-VBRInstantRecovery`, file restore cmdlets), the "snap-in became a module in v11" note, module name, performance and REST API remarks, and the Verify section.
Method: documentation only; no commands were run.
