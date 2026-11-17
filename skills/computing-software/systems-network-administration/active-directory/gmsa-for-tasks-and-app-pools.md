---
id: computing-software.systems-network-administration.active-directory.gmsa-for-tasks-and-app-pools
name: gmsa-for-tasks-and-app-pools
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, gmsa, group-managed-service-account, gmsa-scheduled-task, gmsa-app-pool, scheduled-tasks, iis, new-scheduledtaskprincipal, logontype-password, log-on-as-batch-job]
level: practitioner
status: gated
description: "Run scheduled tasks and IIS application pools as a gMSA: New-ScheduledTaskPrincipal -LogonType Password, batch logon right, app pool identity, and pitfalls."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/manage-group-managed-service-accounts
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/applicationpools/add/processmodel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gMSA for scheduled tasks and IIS app pools

Prerequisite: the gMSA exists and `Test-ADServiceAccount` is True on the host (see the
create-and-install-gmsa skill).

## Scheduled task as a gMSA
Task Scheduler is a supported host for gMSAs; PowerShell example:
```powershell
$action    = New-ScheduledTaskAction -Execute 'pwsh.exe' -Argument '-NoProfile -File <SCRIPTS_DIR>\nightly-report.ps1'
$trigger   = New-ScheduledTaskTrigger -Daily -At 02:00
$principal = New-ScheduledTaskPrincipal -UserId 'AD\gmsaReports$' -LogonType Password -RunLevel Limited
Register-ScheduledTask -TaskName 'Nightly report' -Action $action -Trigger $trigger -Principal $principal
```
- `-LogonType Password` with no password is how a gMSA is specified; the host retrieves it. (gated: unconfirmed, source is paywalled or blocked) No Microsoft page that was readable states this form.
- The gMSA may need **Log on as a batch job** on the host (local policy or GPO). (gated: unconfirmed, source is paywalled or blocked) The Windows Server gMSA pages do not mention the right.
- Grant the gMSA rights to whatever it touches (share/NTFS, SQL logins, AD delegation) like any account.

## IIS application pool as a gMSA
```powershell
Import-Module WebAdministration
Set-ItemProperty IIS:\AppPools\PayrollPool -Name processModel -Value @{userName='AD\gmsaPayroll$'; password=''; identityType=3}
```
(`identityType=3` is SpecificUser.) In IIS Manager: Advanced Settings > Identity > Custom
account > `AD\gmsaPayroll$`, leave password blank. Then:
- For Kerberos to the site under a host name, register the `HTTP/` SPN for that name on the gMSA. The Windows authentication reference notes that `useKernelMode` can matter for pools with a custom identity.
- Web farms: put every farm node in the gMSA's allowed host group.

## Gotchas
- Services that cache credentials themselves or need the plaintext password (some
  third-party apps) cannot use gMSAs.
- Interactive logon with a gMSA is impossible by design.

## Verify
- [ ] `Get-ScheduledTaskInfo 'Nightly report'` LastTaskResult = 0 after a run.
- [ ] App pool worker process runs as the gMSA (`Get-Process w3wp -IncludeUserName`, from an elevated session).

## Checked
Checked 2026-10-27 against Microsoft Learn (gMSA overview and manage articles 07/2025; New-ScheduledTaskPrincipal, Windows Server 2025 reference; IIS processModel reference; Get-Process reference).
- Confirmed: Task Scheduler, Service Control Manager and IIS app pools are supported gMSA hosts; New-ScheduledTaskPrincipal -LogonType accepts Password; processModel identityType SpecificUser has numeric value 3 and userName/password attributes; Get-Process -IncludeUserName.
- Gated: the no-password -LogonType Password form for a gMSA and the batch-logon right requirement.
- Removed: the 0x80070569 error text, the IIS_IUSRS automatic-membership claim and the useAppPoolCredentials setting, which no readable page confirmed.

Method: documentation only; no commands were run.
