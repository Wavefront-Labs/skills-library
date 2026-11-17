---
id: computing-software.systems-network-administration.windows-server.scheduled-tasks-at-scale-with-cimsession
name: scheduled-tasks-at-scale-with-cimsession
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, task-scheduler, scheduledtask-cimsession, cim-sessions, register-scheduledtask, fleet-management]
level: practitioner
status: docs-checked
description: "Manage scheduled tasks on many servers at once with CIM sessions: inventory, register, change and disable tasks remotely using the ScheduledTasks module."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/new-cimsession
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/new-cimsessionoption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled tasks across many servers with CIM sessions

The `ScheduledTasks` cmdlets used here take `-CimSession`, so one session array drives a whole fleet (WS-Management by default).

## Sessions
```powershell
$servers = Get-ADComputer -SearchBase 'OU=Servers,DC=ad,DC=example,DC=com' -Filter 'Enabled -eq $true' | % DNSHostName
$cs = New-CimSession -ComputerName $servers -ErrorAction SilentlyContinue -ErrorVariable failed
$failed                                              # errors for hosts that could not be reached
```
For hosts without WinRM, pass `-SessionOption (New-CimSessionOption -Protocol Dcom)` to `New-CimSession`.

## Inventory
```powershell
Get-ScheduledTask -CimSession $cs | ? { $_.TaskPath -notlike '\Microsoft\*' } |
  Select PSComputerName,TaskPath,TaskName,State,@{n='RunAs';e={$_.Principal.UserId}} |
  Export-Csv tasks.csv -NoTypeInformation
Get-ScheduledTaskInfo -CimSession $cs -TaskPath '\Ops\' -TaskName NightlyCleanup |
  Select PSComputerName,LastRunTime,LastTaskResult,NextRunTime
```

## Deploy the same task everywhere
```powershell
$a = New-ScheduledTaskAction -Execute powershell.exe -Argument '-NoProfile -File <SCRIPTS>\cleanup.ps1'
$t = New-ScheduledTaskTrigger -Daily -At 2am -RandomDelay (New-TimeSpan -Minutes 30)
$p = New-ScheduledTaskPrincipal -UserId SYSTEM -RunLevel Highest
Register-ScheduledTask -CimSession $cs -TaskPath '\Ops\' -TaskName NightlyCleanup -Action $a -Trigger $t -Principal $p -Force
```
The script path must exist on each target; copy it first (`Copy-Item -ToSession` with a PSSession).

## Change and disable
```powershell
Disable-ScheduledTask -CimSession $cs -TaskPath '\Ops\' -TaskName NightlyCleanup
Set-ScheduledTask -CimSession $cs -TaskPath '\Ops\' -TaskName NightlyCleanup -Trigger (New-ScheduledTaskTrigger -Daily -At 3am)
```

## Verify
- [ ] Inventory CSV shows the task on every reachable server with LastTaskResult 0 after the first run.
- [ ] `Remove-CimSession $cs` at the end.

## Checked

2026-10-26 against the ScheduledTasks module reference for Windows Server 2025 (windows-powershell-docs, last commit 2026-10-23), the CimCmdlets reference (PowerShell docs 7.5) and Get-ADComputer: -CimSession on the ScheduledTasks cmdlets, New-ScheduledTaskTrigger -Daily and -RandomDelay, Register-/Set-/Disable-ScheduledTask usage, New-CimSession and New-CimSessionOption -Protocol Dcom, Remove-CimSession, Copy-Item -ToSession, Get-ADComputer -SearchBase and -Filter. Removed the OriginInfo property access, the claim that every cmdlet takes -CimSession, the UNC and PSComputerName remarks as unconfirmed.

Method: documentation only; no commands were run.
