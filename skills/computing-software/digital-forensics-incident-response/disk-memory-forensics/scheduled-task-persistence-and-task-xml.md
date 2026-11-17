---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.scheduled-task-persistence-and-task-xml
name: scheduled-task-persistence-and-task-xml
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [scheduled-task-persistence, scheduled-tasks, persistence, taskcache, 4698, dfir]
level: practitioner
status: docs-checked
description: "Find malicious scheduled task persistence: task XML files, TaskCache registry keys, hidden tasks with the SD value deleted (Tarrask), and 4698 and TaskScheduler logs."
sources: ["https://www.microsoft.com/en-us/security/blog/2022/04/12/tarrask-malware-uses-scheduled-tasks-for-defense-evasion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled task persistence and task XML

**Goal:** enumerate scheduled tasks including those hidden from `schtasks`, and identify the malicious ones.

## Sources (per Microsoft's Tarrask post)
- Registry `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\TASK_NAME` holds `Id`, `Index` and `SD` (security descriptor) values: task registration metadata.
- Registry `...\TaskCache\Tasks\{GUID}`: the GUID maps to the `Id` in the Tree key; holds `Actions`, `Path`, `Triggers` and other execution parameters.
- An extensionless XML file in `System32\Tasks` under the Windows directory, named after the task, with the command in its `<Command>` section. The command is stored both in the XML and in the `Actions` value, so one can recover the task's purpose if the other is wiped.
- Event logs: Event ID 4698 in Security.evtx and Microsoft-Windows-TaskScheduler/Operational.evtx. Neither is audited by default; an administrator must enable them. The Maintenance log exists by default but holds only engine maintenance data.

## Hidden tasks (Tarrask)
- Deleting the `SD` value under the Tree key makes the task disappear from `schtasks /query` and Task Scheduler while it still exists in the registry.
- `reg delete` of `SD` fails with Access Denied even from an elevated prompt; it must run as SYSTEM. Tarrask used token theft from lsass.exe.
- Microsoft's hunt advice: enumerate the TaskCache\Tree hive and find tasks with no `SD` value, then analyse them.
- Removing the Tree and Tasks keys and the XML file would delete the on-disk artefacts, but the task keeps running per its triggers until reboot or until the svchost.exe process running it ends. Microsoft flags long-uptime systems (domain controllers, database servers) as the risk.
- Even for hidden tasks, 4698 and TaskScheduler/Operational events still record them: centralise these logs.

## Practice (not from the cited page)
Compare Tree keys against `schtasks /query` output and the XML files; treat tasks with scripts in user-writable paths, encoded PowerShell, or look-alike Microsoft names as suspect. Tools such as Autoruns and Velociraptor can enumerate tasks.

## Verify
Every suspicious task has a registration time (4698 or Operational log), its action from the XML or `Actions` value, and evidence of execution.

## Checked
Dated 2026-11-08. Confirmed against the Microsoft Tarrask post. Removed: the MITRE T1053/005 source (stub), legacy .job files, XML element lists (Triggers, Principals, ComHandler), Index = 0 heuristic, event IDs 4702, 106, 140, 200/201, and the tool-specific artefact names.
Method: docs-only read of cited pages, 2026-11-08
