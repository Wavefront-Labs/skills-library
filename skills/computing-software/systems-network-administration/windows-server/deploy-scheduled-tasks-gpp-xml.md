---
id: computing-software.systems-network-administration.windows-server.deploy-scheduled-tasks-gpp-xml
name: deploy-scheduled-tasks-gpp-xml
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scheduled-tasks, task-scheduler, scheduled-task-xml, gpp-scheduled-task, export-scheduledtask, schtasks-xml, group-policy-preferences, fleet-deployment]
level: practitioner
status: docs-checked
description: "Distribute the same scheduled task to many servers: export/import task XML with Export-ScheduledTask or schtasks, and Group Policy Preferences Scheduled Tasks."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/export-scheduledtask
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/remove-this-item-if-it-is-no-longer-applied-option
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-preferences
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy scheduled tasks to many machines

## Option A: XML export/import (scriptable)
```powershell
Export-ScheduledTask -TaskPath '\Contoso\' -TaskName 'Sync reports' | Out-File SyncReports.xml -Encoding Unicode
$xml = Get-Content SyncReports.xml -Raw
Invoke-Command -ComputerName (Get-Content servers.txt) {
  Register-ScheduledTask -Xml $using:xml -TaskPath '\Contoso\' -TaskName 'Sync reports' -Force }
```
schtasks equivalent: `schtasks /create /tn "\Contoso\Sync reports" /xml SyncReports.xml /ru SYSTEM /f`
(`/xml` can be combined with `/ru` and `/rp`; `/f` suppresses the warning when the task already exists).
- XML keeps triggers, settings and conditions exactly; edit `<UserId>` for a different principal.
- Do not deploy stored-password tasks this way; prefer a service account such as SYSTEM or a gMSA.

## Option B: Group Policy Preferences
*Computer Configuration > Preferences > Control Panel Settings > Scheduled Tasks* handles scheduled and immediate tasks.
- Run as `NT AUTHORITY\System` so no password has to be stored.
- Use item-level targeting to limit which computers get the item.
- The Common tab option *Remove this item when it is no longer applied* removes settings the item applied once the item
  falls out of scope (for example by targeting or GPO changes). Selecting it sets the action to Replace, and it is not
  available with the Delete action. It relies on a local per-machine database. Without it, preferences do not remove
  settings when a GPO stops applying.
- Never put credentials in GPP tasks.

## Verify
- [ ] `Get-ScheduledTask -TaskPath '\Contoso\*' -CimSession $servers | Group PSComputerName` shows the task on every target.
- [ ] After the GPO stops applying, the task is removed if the remove option was set beforehand.

## Checked

2026-10-26 against the Task Scheduler docs (schtasks create /xml, /ru, /f), the Register-ScheduledTask and Export-ScheduledTask references (Windows Server 2025, last commit 2026-10-23) and Microsoft's troubleshooting article on the GPP remove-this-item option: behaviour and limits of that option and what the Scheduled Tasks extension covers. The previous Group Policy Preferences link returned 404 and was replaced. Removed unconfirmed claims about item names and Update behaviour, the gMSA LogonType XML detail, the cpassword bulletin reference and the -ThrottleLimit value.

Method: documentation only; no commands were run.
