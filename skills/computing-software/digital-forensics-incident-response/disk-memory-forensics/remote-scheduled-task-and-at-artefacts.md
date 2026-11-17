---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.remote-scheduled-task-and-at-artefacts
name: remote-scheduled-task-and-at-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [remote-scheduled-task, scheduled-tasks, lateral-movement, 4698, schtasks, dfir]
level: practitioner
status: draft
description: "Detect scheduled tasks created remotely for lateral movement (schtasks /s, Impacket atexec, at.exe): 4698/4702, TaskScheduler logs, task XML and network logon pairing."
sources: ["https://jpcertcc.github.io/ToolAnalysisResultSheet/", "https://attack.mitre.org/techniques/T1053/005/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote scheduled task and at-job artefacts

**Goal:** prove that a task was registered on a host from another host and ran a payload.

## Destination host
- Security **4698** (task created) with task name, XML content including `Command` and
  `Arguments`, and `SubjectUserName`; 4699 (deleted), 4700/4701 (enabled/disabled), 4702
  (updated). Requires "Audit Other Object Access Events".
- `Microsoft-Windows-TaskScheduler/Operational` 106 (registered), 140 (updated), 141
  (deleted), 200/201 (action started/completed), 129 (process created with PID).
- Security 4624 type 3 from the source just before, plus 5145 access to `\\*\IPC$` named
  pipe `atsvc` (for `at`/Impacket atexec).
- Task XML file in `Windows\System32\Tasks\<name>` (author, registration date, command)
  and registry `SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\<name>`.
- Impacket `atexec.py`: random 8-char task name, runs `cmd.exe /C <cmd> > %windir%\Temp\<rand>.tmp 2>&1`,
  task deleted after (4699 shortly after 4698).

## Source host
`schtasks.exe /create /s <target> /u ... /tr ...` in 4688/Sysmon 1, Prefetch SCHTASKS.EXE,
4648 explicit credentials naming target; PowerShell `Register-ScheduledTask -CimSession`.

## Hunt
```kusto
SecurityEvent | where EventID == 4698
| extend Cmd = extract(@"<Command>(.*?)</Command>", 1, EventData)
| where Cmd has_any ("cmd.exe","powershell","\\Temp\\","rundll32")
```

## Gotchas
- Deleted tasks leave 4699/141 and possibly TaskCache remnants; the XML file is removed.
- Legitimate software creates many tasks; focus on created-then-deleted pairs and those
  created by remote logons.

## Verify
4624 type 3 from source, 4698 within seconds, 200/129 showing execution, and 4699 if
cleaned, all for the same task name.
