---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.powershell-remoting-and-winrm-artefacts
name: powershell-remoting-and-winrm-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [winrm, powershell-remoting, lateral-movement, wsmprovhost, 4104, dfir]
level: practitioner
status: draft
description: "Detect PowerShell Remoting and WinRM lateral movement (Enter-PSSession, Invoke-Command, evil-winrm): wsmprovhost, WinRM logs, 4624 type 3 and script block logs."
sources: ["https://jpcertcc.github.io/ToolAnalysisResultSheet/", "https://attack.mitre.org/techniques/T1021/006/", "https://learn.microsoft.com/en-us/powershell/scripting/learn/remoting/running-remote-commands"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PowerShell remoting and WinRM artefacts

**Goal:** prove remote execution over WinRM (TCP 5985/5986) and recover the commands run.

## Destination host
- Process: `wsmprovhost.exe` (parent `svchost.exe -k DcomLaunch`) hosting the remote
  session; children are the commands' processes.
- Security 4624 type 3 with the account, from source IP; 4672 for admins.
- `Microsoft-Windows-WinRM/Operational`: 91 (session created, user), 168 (auth),
  142/169.
- `Microsoft-Windows-PowerShell/Operational`: **4104 script block** with the actual code
  executed remotely (if logging enabled), 4103 module logging; 40961/40962 (PowerShell
  console starting) in `Windows PowerShell` log 400/403 with `HostName=ServerRemoteHost`.
- Prefetch `WSMPROVHOST.EXE`.

## Source host
- `Microsoft-Windows-WinRM/Operational` 6 (creating WSMan session, **destination name**),
  8, 15, 16, 33.
- PowerShell 4104 containing `Enter-PSSession`/`Invoke-Command -ComputerName`/`New-PSSession`.
- `ConsoleHost_history.txt` in `AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\`.
- 4648 explicit credential use naming the target.
- evil-winrm runs from Linux/Ruby: only destination artefacts remain; its use shows
  `wsmprovhost.exe` children and uploads via base64 chunks in 4104.

## Hunt
```kusto
DeviceProcessEvents | where InitiatingProcessFileName =~ "wsmprovhost.exe"
| summarize count() by DeviceName, AccountName, FileName
```
Baseline admin use (configuration management tools such as Ansible Windows modules use WinRM).

## Verify
Destination WinRM 91 and wsmprovhost process start align with source WinRM 6 to the same
host name and the 4624 type 3 logon.
