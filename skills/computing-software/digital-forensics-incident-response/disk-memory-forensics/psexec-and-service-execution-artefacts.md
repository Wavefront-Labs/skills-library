---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.psexec-and-service-execution-artefacts
name: psexec-and-service-execution-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [psexec, lateral-movement, service-execution, 7045, impacket, dfir]
level: practitioner
status: draft
description: "Identify PsExec and service-based remote execution (Sysinternals PsExec, Impacket psexec/smbexec, Cobalt Strike) on source and destination hosts from logs and files."
sources: ["https://jpcertcc.github.io/ToolAnalysisResultSheet/", "https://www.sans.org/posters/hunt-evil/", "https://attack.mitre.org/techniques/T1569/002/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PsExec and service execution artefacts

**Goal:** prove remote command execution via SMB + service creation, identify source host,
account and commands.

## Destination host
| Artefact | Sysinternals PsExec | Impacket psexec.py / smbexec.py / CS `jump psexec` |
|---|---|---|
| Security 4624 | Type 3 logon from source IP with the used account (4672 if admin) | Same |
| Security 5140/5145 | Share `ADMIN$` / `IPC$` accessed | Same; `C$` for some tools |
| System 7045 | Service `PSEXESVC` installed, ImagePath `%SystemRoot%\PSEXESVC.exe` (renamable with `-r`) | Random 4-8 char or random-looking service name; ImagePath like `%COMSPEC% /Q /c echo ... ^> \\127.0.0.1\C$\__output` (smbexec) or random `.exe` in `ADMIN$` (psexec.py); CS uses random 7-char names and `\\127.0.0.1\ADMIN$\<rand>.exe` or PowerShell one-liners |
| Files | `Windows\PSEXESVC.exe`, Prefetch `PSEXESVC.EXE-*.pf` | Random exe in `Windows\`, `__output` temp files |
| Named pipes | `\PSEXESVC`, `-stdin/-stdout/-stderr` pipes | `\RemCom_*` (psexec.py) |
| Registry | `SYSTEM\...\Services\PSEXESVC` | Services key of random name (often deleted after) |
Newer PsExec versions also create `PSEXEC-<SOURCEHOST>-<random>.key` files in `Windows\`,
revealing the **source hostname**.

## Source host
Prefetch `PSEXEC.EXE`/`PSEXEC64.EXE`, `HKCU\Software\Sysinternals\PsExec\EulaAccepted`,
Security 4648 (explicit credentials) with target server name, command history, Python
artefacts for Impacket.

## Hunt
```kusto
SecurityEvent | where EventID == 7045 | where ImagePath has_any ("ADMIN$","\\\\127.0.0.1","%COMSPEC%","powershell -nop")
```
Sigma rules exist for PSEXESVC, Impacket service patterns, and CS service names.

## Verify
For each destination: 4624 type 3 from source, 7045 service creation seconds later, process
execution of the service binary (4688/Sysmon 1), all with consistent times and account.
