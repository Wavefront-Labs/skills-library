---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.dcom-lateral-movement-artefacts
name: dcom-lateral-movement-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [dcom-lateral-movement, lateral-movement, wmi-lateral-movement, windows-event-logs, dfir]
level: advanced
status: draft
description: "Detect DCOM-based lateral movement (MMC20.Application, ShellWindows, ShellBrowserWindow, Excel): process trees, logon events, RPC traffic and registry traces."
sources: ["https://attack.mitre.org/techniques/T1021/003/", "https://www.cybereason.com/blog/dcom-lateral-movement-techniques"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DCOM lateral movement artefacts

**Goal:** attackers instantiate COM objects on remote hosts over DCOM (ATT&CK T1021.003) to run
commands without PsExec services or WMI process creation.

## Common objects
| Object (ProgID / CLSID) | Method | Child process parent on target |
|---|---|---|
| `MMC20.Application` {49B2791A-B1AE-4C90-9B8E-E860BA07F889} | `Document.ActiveView.ExecuteShellCommand` | `mmc.exe` -> cmd/powershell |
| `ShellWindows` {9BA05972-F6A8-11CF-A442-00A0C90A8F39} | `Item().Document.Application.ShellExecute` | `explorer.exe` -> child |
| `ShellBrowserWindow` {C08AFD90-F2A1-11D1-8455-00A0C91F3880} | same | `explorer.exe` |
| `Excel.Application` | `DDEInitiate`, `RegisterXLL` | `excel.exe` -> child |
| `Outlook.Application`, `Visio` etc. | various | Office process |

## Target-side evidence
- **Process creation (4688 / Sysmon 1):** unusual children of `mmc.exe` (with `-Embedding` in
  its command line), `explorer.exe` children with no user interaction, `excel.exe /automation -Embedding`.
- `DcomLaunch` service (svchost) parents the COM server process (`mmc.exe -Embedding`).
- **Logons:** 4624 logon type 3 from the source host just before, by the attacker account; 4672 if admin.
- System log 10016/10028 DCOM errors when attempts fail (permissions, hardening from KB5004442).

## Source-side evidence
- PowerShell 4104 script blocks with `[activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application","target"))`.
- Network: RPC endpoint mapper TCP 135 then dynamic high port to the target (Zeek `dce_rpc.log` shows `ISystemActivator RemoteCreateInstance`).

## Hunting query idea
```text
ParentImage endswith \mmc.exe and ParentCommandLine contains "-Embedding" and Image in (cmd.exe, powershell.exe, rundll32.exe)
```

## Gotchas
- Office automation is legitimate in some environments (reporting servers); baseline first.
- DCOM hardening changes (2022-2023) cause some techniques to fail; failed attempts still leave 10016/10036 events.

## Verify
Pair each suspicious target-side process with a type-3 logon from the source and source-side tooling evidence.
