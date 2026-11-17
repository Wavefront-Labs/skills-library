---
id: computing-software.it-support-helpdesk.desktop-support.task-scheduler-for-support-tasks
name: task-scheduler-for-support-tasks
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-admin-tools, task-scheduler, schtasks, register-scheduledtask, scheduled-task-history, run-whether-logged-on, last-run-result, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Create and debug Windows scheduled tasks: triggers, run-as accounts and 'run whether user is logged on', schtasks/PowerShell, task history, last run result codes, and rogue tasks."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-query"
  - "https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask"
  - "https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal"
  - "https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# task-scheduler-for-support-tasks

Goal: run a script or tool on a schedule or event reliably, and find out why
an existing task "does not run".

## Create
```powershell
$a = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -File "%ProgramData%\Corp\cleanup.ps1"'
$t = New-ScheduledTaskTrigger -Daily -At 12:30
$p = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest
Register-ScheduledTask -TaskName 'Corp\TempCleanup' -Action $a -Trigger $t -Principal $p
```
```cmd
schtasks /create /tn "Corp\TempCleanup" /tr "powershell.exe -File %ProgramData%\Corp\cleanup.ps1" /sc daily /st 12:30 /ru SYSTEM
schtasks /run /tn "Corp\TempCleanup"
schtasks /query /tn "Corp\TempCleanup" /v /fo list
```
(Replace the example script path with your own.) `/st` uses 24-hour HH:mm,
`/sc daily` runs every day by default, and a task created with `/ru SYSTEM`
shows Run As User `NT AUTHORITY\SYSTEM` and Logon Mode "Background only" in
the verbose query. `/v` is valid with LIST or CSV output.

## Debug
- **Last Run Result** (`schtasks /query /v /fo list`, or the Task Scheduler
  console): `0x41301` means the task is currently running; `0x41303` means the
  task has not yet run. For other codes use Microsoft's Task Scheduler error
  and success constants and the Win32 error list.
- Run the exact action line by hand as the same account to see its errors.
- Wrap scripts with logging (`Start-Transcript`).

## Gotchas
- The account a task runs as decides which files and network resources it can
  reach; SYSTEM runs in the background with no interactive user.
- A task you do not recognise should be reported to security instead of
  deleted.

## Verify
`schtasks /query /tn <name> /v /fo list` shows the expected next and last run
time and a success result.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn schtasks create/query/run, Register-ScheduledTask and New-ScheduledTaskPrincipal pages and Task Scheduler error constants, as published October 2026. Confirmed: schtasks /create, /tn, /tr, /sc, /st, /ru SYSTEM behaviour, /query /v /fo, Register-ScheduledTask -TaskName and -Principal, New-ScheduledTaskPrincipal -RunLevel, result codes 0x41301 and 0x41303. Removed: 0x0/0x1/0x2/0x800710E0 meanings, run-whether-logged-on and AC-power condition claims, history-enable menu path, event triggers, and the persistence advice.

Run 2026-11-01 (read-only): `schtasks /query /v /fo list` on a built-in task printed Last Result, Run As User `SYSTEM` and Logon Mode; `/v` with `/fo table` also works. Task creation (schtasks and PowerShell) was not run because it changes the machine, so the skill stays docs-checked.
Method: documentation plus read-only queries.
