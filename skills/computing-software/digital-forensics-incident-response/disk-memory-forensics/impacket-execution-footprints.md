---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.impacket-execution-footprints
name: impacket-execution-footprints
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [impacket-footprints, lateral-movement, psexec, wmi-lateral-movement, windows-event-logs, dfir]
level: advanced
status: draft
description: "Recognise Impacket psexec, smbexec, wmiexec, atexec and dcomexec on targets: service names, output redirection files, process trees and event IDs."
sources: ["https://github.com/fortra/impacket", "https://attack.mitre.org/software/S0357/", "https://www.jpcert.or.jp/english/pub/sr/ir_research.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Impacket execution footprints

**Goal:** Impacket (ATT&CK S0357) is the most common offensive Python toolkit for remote
execution. Each script leaves a distinctive pattern on the target.

## Patterns
| Script | Mechanism | Target artefacts |
|---|---|---|
| `psexec.py` | Uploads a service binary (RemComSvc) to ADMIN$, creates service | 7045 with random 4-char service name and random EXE name in `%SystemRoot%`; named pipes `RemCom_stdin/stdout/stderr`; 5145 share access to ADMIN$ |
| `smbexec.py` | Creates a service per command whose binPath is `%COMSPEC% /Q /c echo <cmd> ^> \\127.0.0.1\C$\__output 2^>^&1 > %TEMP%\execute.bat & %COMSPEC% /Q /c %TEMP%\execute.bat & del %TEMP%\execute.bat` | 7045 per command, service name default `BTOBTO` (older) or random; `execute.bat`; `__output` file |
| `wmiexec.py` | `Win32_Process.Create` via WMI: `cmd.exe /Q /c <cmd> 1> \\127.0.0.1\ADMIN$\__<epoch> 2>&1` | `WmiPrvSE.exe` -> `cmd.exe /Q /c ...` with `\\127.0.0.1\ADMIN$\__1697...` output; 4624 type 3 |
| `atexec.py` | Creates a scheduled task via ATSVC, runs, deletes | 4698/4699 task created and deleted within seconds, random 8-char task name; output to `%SystemRoot%\Temp\<random>.tmp` |
| `dcomexec.py` | MMC20 / ShellWindows / ShellBrowserWindow | `mmc.exe -Embedding` or `explorer.exe` children with the same output redirection pattern |
| `secretsdump.py` | Remote registry + `reg save` to temp, or DRSUAPI | RemoteRegistry service start, SAM/SECURITY saved to `%SystemRoot%\Temp\<random>.tmp`, 4662 for DCSync |

## Hunting
```text
CommandLine contains "\\127.0.0.1\ADMIN$\__" or CommandLine contains "\\127.0.0.1\C$\__output"
ServiceFileName contains "%COMSPEC% /Q /c echo"  (7045)
```
- Look for 4624 type 3 with NTLM from Linux workstation names or random names (Impacket default
  workstation name is often blank or random).

## Gotchas
- Forks and renamed copies change defaults (service names, output share); the redirect-to-share pattern is the robust indicator.
- Output files are deleted after read; recover from MFT/USN (`$UsnJrnl` shows `__<epoch>` create/delete).

## Verify
Tie each footprint to a source IP/workstation in 4624 and to the attacker account.
