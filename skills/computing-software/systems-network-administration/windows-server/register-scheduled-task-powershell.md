---
id: computing-software.systems-network-administration.windows-server.register-scheduled-task-powershell
name: register-scheduled-task-powershell
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scheduled-tasks, task-scheduler, register-scheduledtask, new-scheduledtasktrigger, new-scheduledtaskaction, new-scheduledtasksettingsset, scheduledtasks-module, repetition-interval, automation]
level: practitioner
status: docs-checked
description: "Create scheduled tasks with the ScheduledTasks module: actions with working directory, daily/startup/repeating triggers, settings (timeouts, no overlap) and registration."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasktrigger
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/tasksettings-executiontimelimit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create scheduled tasks with PowerShell

```powershell
$action = New-ScheduledTaskAction -Execute 'pwsh.exe' `
  -Argument '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "<SCRIPTS_DIR>\Sync-Reports.ps1"' `
  -WorkingDirectory '<SCRIPTS_DIR>'
$triggers = @(
  New-ScheduledTaskTrigger -Daily -At '02:30'
  New-ScheduledTaskTrigger -AtStartup
)
# repeat every 15 minutes; -RepetitionDuration sets how long the pattern repeats
$rep = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 15)
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
  -MultipleInstances IgnoreNew -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5) `
  -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName 'Sync reports' -TaskPath '\Contoso\' -Action $action `
  -Trigger $triggers -Settings $settings -Principal $principal -Description 'Owner: ops; CHG1234' -Force
```
- `-Force` runs the operation without prompting for confirmation.
- Use a **task folder** (`-TaskPath '\Contoso\'`) to keep your tasks separate from Microsoft's.
- A task is stopped 72 hours after it starts by default; set `-ExecutionTimeLimit` to a realistic limit.
- `MultipleInstances IgnoreNew` prevents overlapping runs.
- Quote paths with spaces inside `-Argument`.

## Run, inspect, change
```powershell
Start-ScheduledTask -TaskPath '\Contoso\' -TaskName 'Sync reports'
Get-ScheduledTaskInfo -TaskPath '\Contoso\' -TaskName 'Sync reports'   # LastRunTime, LastTaskResult, NextRunTime
Get-ScheduledTask -TaskPath '\Contoso\*' | Select TaskName,State
Disable-ScheduledTask -TaskPath '\Contoso\' -TaskName 'Sync reports'
Unregister-ScheduledTask -TaskPath '\Contoso\' -TaskName 'Sync reports' -Confirm:$false
```
Remote: all cmdlets take `-CimSession server01`.

## Gotchas
- Set `-WorkingDirectory` on the action when the script uses relative paths.

## Verify
- [ ] `Get-ScheduledTaskInfo` shows NextRunTime as expected and LastTaskResult 0 after a manual start.

## Checked

2026-10-26 against the ScheduledTasks module reference for Windows Server 2025 (windows-powershell-docs, last commit 2026-10-23) and the Task Scheduler docs (win32, last commit 2026-10-08): parameter names of New-ScheduledTaskAction (-Execute, -Argument, -WorkingDirectory), New-ScheduledTaskTrigger (-RepetitionInterval, -RepetitionDuration, -Once, -AtStartup, -Daily), New-ScheduledTaskSettingsSet, New-ScheduledTaskPrincipal (-LogonType ServiceAccount, -RunLevel Highest), Register-ScheduledTask (-TaskPath, -Description, -Force), the 72 hour default time limit, and the MultipleInstances values. Corrected -Force (documented as suppressing confirmation, not overwriting) and removed unconfirmed claims about default working directory, exit-code mapping and the SYSTEM network identity.

Method: documentation only; no commands were run.
