---
id: computing-software.systems-network-administration.windows-server.scheduled-task-troubleshooting
name: scheduled-task-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scheduled-tasks, task-scheduler, task-last-run-result, task-scheduler-history, 0x1, 0x41301, 0x8007052e, 0x800710e0, taskscheduler-operational-log, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug scheduled tasks: decode LastTaskResult codes (0x1, 0x41301, 0x8007052E...), enable and query the TaskScheduler Operational history, and common causes."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants
  - https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1300-1699-
  - https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--4000-5999-
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wevtutil
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Scheduled task troubleshooting

## Result codes (LastTaskResult)
| Code | Meaning (source) |
|---|---|
| 0x0 | success |
| 0x1 | Win32 error 1, ERROR_INVALID_FUNCTION (incorrect function); debug the command itself |
| 0x2 | ERROR_FILE_NOT_FOUND: check the path in Execute and Arguments |
| **0x41301** | SCHED_S_TASK_RUNNING: the task is currently running |
| 0x41303 | SCHED_S_TASK_HAS_NOT_RUN: the task has not yet run |
| 0x41306 | SCHED_S_TASK_TERMINATED: the last run was terminated by the user |
| 0x800710E0 | ERROR_REQUEST_REFUSED (0x10E0): the operator or administrator has refused the request |
| **0x8007052E** | ERROR_LOGON_FAILURE (0x52E): logon failure, for example a wrong or changed stored password |
| 0x80070569 | ERROR_LOGON_TYPE_NOT_GRANTED (0x569): the account has not been granted the requested logon type; Task Scheduler also notes that the task principal needs batch logon privilege (SCHED_S_BATCH_LOGON_PROBLEM, 0x4131C) |
| 0x80070005 | ERROR_ACCESS_DENIED: the identity lacks rights on files or registry |
## History log
The operational log is Microsoft-Windows-TaskScheduler/Operational; it may need enabling:
```cmd
wevtutil set-log Microsoft-Windows-TaskScheduler/Operational /e:true
```
```powershell
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-TaskScheduler/Operational'} -MaxEvents 50 |
  ? Message -match 'Sync reports' | ft TimeCreated,Id,Message -Wrap
```
Read the event text for the task name and result; this skill does not list event IDs.

## Debug the action itself
Run the exact command line as the task identity, or temporarily add output redirection or `Start-Transcript` to the
script. Set `New-ScheduledTaskAction -WorkingDirectory` when the script uses relative paths.

## Verify
- [ ] `Get-ScheduledTaskInfo` shows LastTaskResult 0 for the latest run.
- [ ] Task history retained (log size adequate) for audit.

## Checked

2026-10-26 against the Task Scheduler docs (win32 error and success constants, system error codes 0-499, 1300-1699 and 4000-5999; last commit 2026-10-08) and the wevtutil reference (set-log /e): result codes 0x41301, 0x41303, 0x41306, 0x4131C, Win32 codes 0x2, 0x5, 0x52E, 0x569 and 0x10E0, the operational log name and the enable command. Removed unconfirmed per-code causes, the event ID list, the psexec suggestion, the mapped-drive claim and 0xC000013A.

Method: documentation only; no commands were run.
