---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.wmi-remote-execution-artefacts
name: wmi-remote-execution-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [wmi-lateral-movement, wmi, lateral-movement, wmiprvse, wmic, dfir]
level: practitioner
status: draft
description: "Identify WMI remote execution (wmic process call create, Invoke-WmiMethod, Impacket wmiexec) on source and destination from process trees, events and WMI logs."
sources: ["https://jpcertcc.github.io/ToolAnalysisResultSheet/", "https://attack.mitre.org/techniques/T1047/", "https://www.sans.org/posters/hunt-evil/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WMI remote execution artefacts

**Goal:** prove commands were executed remotely via WMI (Win32_Process Create) and from where.

## Destination host
- **Process tree**: `WmiPrvSE.exe` (parent `svchost.exe -k DcomLaunch`) spawning
  `cmd.exe`/`powershell.exe`/payload. Impacket `wmiexec.py` pattern:
  `cmd.exe /Q /c <command> 1> \\127.0.0.1\ADMIN$\__<epoch>.<rand> 2>&1`.
- Security 4624 type 3 from source (account, IP), 4672 admin.
- `Microsoft-Windows-WMI-Activity/Operational`: Event 5857 (provider loaded), 5860/5861
  (temporary/permanent event consumers, more for persistence), and on newer builds query
  operations in 5858 errors.
- Prefetch for `WMIPRVSE.EXE` and the launched binaries; 4688/Sysmon 1 with parent
  WmiPrvSE.
- Network: DCOM/RPC on TCP 135 then high dynamic port from source.

## Source host
- `wmic.exe` Prefetch and command line (`wmic /node:10.0.0.5 /user:... process call create "..."`),
  4648 explicit credentials event naming target, PowerShell 4104 with `Invoke-WmiMethod`/
  `Invoke-CimMethod -ComputerName`, Impacket Python on attacker Linux (not on Windows).

## Hunt
```kusto
DeviceProcessEvents
| where InitiatingProcessFileName =~ "wmiprvse.exe"
| where FileName in~ ("cmd.exe","powershell.exe","rundll32.exe","mshta.exe")
| project Timestamp, DeviceName, AccountName, ProcessCommandLine
```
Legitimate management (SCCM, monitoring agents) also spawns from WmiPrvSE; baseline per host
role.

## Gotchas
- No service creation and no files by default, so only process ancestry and logon events
  remain; 4688 with command line or EDR is essential.
- WMI-Activity log does not log remote process creation by itself.

## Verify
Destination 4624 type 3 and WmiPrvSE child process occur within seconds, using the same
account seen in the source's 4648 event.
