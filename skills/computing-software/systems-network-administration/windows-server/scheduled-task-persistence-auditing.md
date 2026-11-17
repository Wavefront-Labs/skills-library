---
id: computing-software.systems-network-administration.windows-server.scheduled-task-persistence-auditing
name: scheduled-task-persistence-auditing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [scheduled-tasks, event-4698, task-persistence, security-auditing, threat-hunting]
level: advanced
status: docs-checked
description: "Hunt and audit scheduled tasks used for persistence: events 4698/4702/4699, suspicious actions and principals, hidden tasks with missing SD and fleet baselines."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698
  - https://www.microsoft.com/en-us/security/blog/2022/04/12/tarrask-malware-uses-scheduled-tasks-for-defense-evasion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing scheduled tasks for persistence

Attackers love tasks: run as SYSTEM, survive reboots, blend in with vendor updaters.

## Turn on auditing
Advanced Audit Policy > Object Access > **Audit Other Object Access Events**. Security event **4698** (a scheduled task
was created) is logged under that subcategory and includes the task name and the full task XML (`TaskContent`).
Also enable and collect the Microsoft-Windows-TaskScheduler/Operational log. Microsoft's guidance for 4698: monitor all
task creation, especially on critical computers; watch for new tasks in the Task Scheduler Library root; and alert when
the task XML contains `<LogonType>Password</LogonType>`, because the account password is then saved in Credential
Manager in cleartext and can be extracted with administrative privileges.

## Hunt on a host
```powershell
Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\Microsoft\*' } | ForEach-Object {
  [pscustomobject]@{Path=$_.TaskPath+$_.TaskName; RunAs=$_.Principal.UserId; Level=$_.Principal.RunLevel
    Action=($_.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)" }) -join ' | '} } | Format-Table -Wrap
```
Red flags: actions that run encoded or download-and-run commands, binaries in user-writable folders, odd names mimicking
real tasks, and tasks created recently on servers without a change.

## Hidden tasks (Tarrask technique)
Microsoft's Tarrask write-up: the malware deletes the `SD` value under
`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\<task name>`. Doing so needs SYSTEM context
(the malware stole a token from lsass.exe; plain `reg delete` failed even when elevated). Without the SD value the task
no longer appears in `schtasks /query` or Task Scheduler, though it keeps running. Detection: enumerate the Tree key and
flag tasks with no SD value, collect 4698 and the TaskScheduler Operational log (they record task activity even for
hidden tasks), and watch outbound connections from Tier 0 and Tier 1 assets. Microsoft Defender detects the behaviour as
Behavior:Win32/ScheduledTaskHide.A.

## Baseline the fleet
Export task names + action hash per server weekly and diff; vendor tasks appear in many servers, singletons deserve a
look.

## Verify
- [ ] 4698 events reach the SIEM with the TaskContent field; alert on creation on critical servers.

## Checked

2026-10-26 against Microsoft's event 4698 reference (archived Windows 10 docs) and the Microsoft Security blog post on Tarrask (12 April 2022): 4698 subcategory and TaskContent field, the monitoring recommendations, the SD value under TaskCache Tree, SYSTEM requirement, visibility effect, detection advice and the Defender detection name. Removed the event IDs 4699 to 4702 and Operational IDs 106, 140, 141, 200 and 201, the System32 Tasks folder comparison and the list of named binaries as unconfirmed.

Method: documentation only; no commands were run.
