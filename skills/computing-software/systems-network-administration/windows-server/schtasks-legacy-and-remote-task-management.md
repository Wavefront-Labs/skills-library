---
id: computing-software.systems-network-administration.windows-server.schtasks-legacy-and-remote-task-management
name: schtasks-legacy-and-remote-task-management
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, task-scheduler, schtasks, remote-management, scheduled-tasks]
level: practitioner
status: docs-checked
description: "Use schtasks.exe for scheduled tasks where PowerShell is unavailable or older: create, query, run, export XML and manage remote machines with /S."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-query
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-change
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# schtasks.exe for legacy and remote management

Use `ScheduledTasks` cmdlets when you can; schtasks works from cmd and batch files and has `/s`, `/u` and `/p` options
for remote computers.

## Common commands
```cmd
schtasks /create /tn "Ops\NightlyCleanup" /tr "powershell.exe -NoProfile -File <SCRIPTS>\cleanup.ps1" ^
  /sc daily /st 02:00 /ru SYSTEM /rl HIGHEST /f
schtasks /query /tn "Ops\NightlyCleanup" /v /fo list
schtasks /run /tn "Ops\NightlyCleanup"
schtasks /end /tn "Ops\NightlyCleanup"
schtasks /change /tn "Ops\NightlyCleanup" /disable
schtasks /delete /tn "Ops\NightlyCleanup" /f
```
With `/ru "AD\svc-task"` and no `/rp`, schtasks prompts for the password; `/ru SYSTEM` needs no password. `/rl` accepts LIMITED or HIGHEST.

## XML round trip (copy a task between servers)
```cmd
schtasks /query /tn "\Ops\NightlyCleanup" /xml > cleanup.xml
schtasks /create /tn "Ops\NightlyCleanup" /xml cleanup.xml /ru SYSTEM /f
```
`/query /xml` needs the full task path and name; `/create /xml` can be combined with `/ru` and `/rp`.

## Remote
```cmd
schtasks /query /s SRV01 /u AD\admin /fo csv /nh
```
The account given with `/u` must be a member of the Administrators group on the remote computer; without `/p` schtasks
prompts for the password.

## Inventory across servers
```cmd
for /f %s in (servers.txt) do schtasks /query /s %s /fo csv /v /nh >> tasks.csv
```
Use `/v` to include advanced properties, including the account each task runs as.

## Gotchas
- `/tn` names with spaces need quotation marks; `/tr` paths are limited to 262 characters.
- `/st` uses 24 hour HH:mm format; the `/sd` and `/ed` date format varies with the system locale (use XML to avoid this).
- Last result codes: 0x0 success, 0x41301 task running, 0x8007010B is Win32 ERROR_DIRECTORY (invalid directory name).

## Verify
- [ ] `schtasks /query /v` shows Last Result 0x0 after a run.

## Checked

2026-10-26 against the Windows Server docs for schtasks, schtasks-create, -query, -run, -end, -change and -delete (windowsserverdocs, last commit 2026-10-23) and the Task Scheduler error constants: /create options (/sc, /tn, /tr, /st, /ru, /rp, /rl, /f, /xml), /query options (/v, /fo, /nh, /xml, /s, /u, /p), /change /disable, /delete /f, /run, /end, the 262 character /tr limit, locale-dependent dates, ERROR_DIRECTORY. Removed unconfirmed claims about RPC transport, WinPE, the firewall group, quote escaping and the meaning of 0x1.

Run 2026-11-01 (read-only, one built-in task): `schtasks /query /tn <full path> /v /fo list` showed Next Run Time, Last Result, Run As User and Logon Mode; `/fo csv /nh` printed a row; `/query /xml` needs the full task path (the bare name failed with "cannot find the file specified"). Create, run, end, change, delete, `/s` remote and XML re-import were not run (they change the machine), so the skill stays docs-checked.
Method: documentation plus read-only queries.
