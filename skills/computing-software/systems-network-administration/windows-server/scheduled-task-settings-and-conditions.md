---
id: computing-software.systems-network-administration.windows-server.scheduled-task-settings-and-conditions
name: scheduled-task-settings-and-conditions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [scheduled-tasks, task-settings, multipleinstances, new-scheduledtasksettingsset, task-scheduler]
level: practitioner
status: docs-checked
description: "Set scheduled task settings correctly: MultipleInstances, ExecutionTimeLimit, restart on failure, start when available, network and power conditions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/tasksettings
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants
  - https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--4000-5999-
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled task settings and conditions

Most "the task did not run" tickets are settings, not triggers.

## Build the settings object
```powershell
$set = New-ScheduledTaskSettingsSet `
  -MultipleInstances IgnoreNew `
  -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
  -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 10) `
  -StartWhenAvailable `
  -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
  -RunOnlyIfNetworkAvailable
Set-ScheduledTask -TaskName 'Nightly Export' -Settings $set
```

## What each one does
| Setting | Default | Notes |
|---|---|---|
| MultipleInstances | IgnoreNew | `Parallel`, `Queue`, `StopExisting` in the task schema (`New-ScheduledTaskSettingsSet` documents IgnoreNew, Parallel and Queue). With IgnoreNew a new instance is not started while one is running |
| ExecutionTimeLimit | 72 h | task is stopped after this; `PT0S` = runs indefinitely |
| RestartCount/Interval | off | number of restart attempts and how long Task Scheduler attempts to restart; set both together |
| StartWhenAvailable | off | the task can start any time after its scheduled time has passed; started tasks are queued with a default delay of 10 minutes |
| DisallowStartIfOnBatteries | on | task is not started if the computer is on batteries (PowerShell parameter is `-AllowStartIfOnBatteries` to permit it) |
| RunOnlyIfIdle / IdleSettings | off | run only if the computer is idle |
| RunOnlyIfNetworkAvailable | off | |
| WakeToRun | off | wakes the computer to run the task |
| Priority | 7 | 0 (highest) to 10 (lowest); 7 and 8 are used for background tasks, 4 to 6 for interactive tasks |
| Hidden | off | hides the task in the UI; an administrator master switch can show all tasks |

## Gotchas
- Last Run Result 0x41306 (SCHED_S_TASK_TERMINATED) is documented as the last run being terminated by the user.
- 0x800710E0 is Win32 ERROR_REQUEST_REFUSED (4320): the operator or administrator refused the request.
- `-Compatibility` accepts At, V1, Vista, Win7 and Win8.

## Verify
```powershell
(Get-ScheduledTask 'Nightly Export').Settings | Format-List MultipleInstances,ExecutionTimeLimit,StartWhenAvailable,RestartCount
```
- [ ] Task history shows runs at expected times.

## Checked

2026-10-26 against the Task Scheduler docs (win32 TaskSettings pages and error constants, last commit 2026-10-08) and the New-ScheduledTaskSettingsSet reference for Windows Server 2025 (last commit 2026-10-23): settings names, the defaults (72 h limit, priority 7, IgnoreNew, StartWhenAvailable off with a 10 minute queue delay, DisallowStartIfOnBatteries true), priority ranges, Compatibility values, 0x41306 meaning and ERROR_REQUEST_REFUSED 0x10E0. Removed unconfirmed claims that restarts apply only to failures to start, that 0x41306 covers the time limit, and that 0x800710E0 means battery or idle conditions.

Method: documentation only; no commands were run.
