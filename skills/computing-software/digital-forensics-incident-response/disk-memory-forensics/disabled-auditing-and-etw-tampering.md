---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.disabled-auditing-and-etw-tampering
name: disabled-auditing-and-etw-tampering
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [etw-tampering, anti-forensics, audit-policy, log-clearing, dfir]
level: advanced
status: draft
description: "Detect audit policy changes, event log service tampering, ETW provider/session disabling and Defender telemetry blinding: events, registry and gaps."
sources: ["https://attack.mitre.org/techniques/T1562/002/", "https://attack.mitre.org/techniques/T1562/006/", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4719"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disabled auditing and ETW tampering

**Goal:** instead of clearing logs (noisy, event 1102), careful attackers stop logs being written
(ATT&CK T1562.002 Disable Windows Event Logging, T1562.006 Indicator Blocking).

## Techniques and evidence
| Technique | Evidence |
|---|---|
| `auditpol /set /category:* /success:disable` | Security **4719** (system audit policy changed); `auditpol` process creation; then silence |
| Stop/disable EventLog service | System 7036/7040 for "Windows Event Log"; 1100 "event logging service has shut down" |
| Kill EventLog threads (Phant0m, Invoke-Phant0m) | Service still "running" but no new events; gaps in normally constant event streams; tool artefacts |
| Disable specific channels | `wevtutil sl Microsoft-Windows-Sysmon/Operational /e:false`; registry `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WINEVT\Channels\<ch>\Enabled = 0` |
| Remove ETW autologger / provider | `HKLM\SYSTEM\CurrentControlSet\Control\WMI\Autologger\<session>\{provider}` `Enabled = 0` (e.g. `EventLog-Application`, Defender `DefenderApiLogger`) |
| Patch `EtwEventWrite` in-process | No log artefact; detect in memory (patched ntdll bytes) or via EDR "ETW tampering" alerts |
| Sysmon unload | `fltMC unload SysmonDrv`; Sysmon event 4 (service state) / 16 config change; driver unload |
| PowerShell logging disabled | Registry `ScriptBlockLogging` policy removed; 4104 stops |

## Hunting for gaps
- Plot event counts per host per hour for always-on channels (Security 4624/4634, Sysmon 1).
  Hosts that go quiet while still online (EDR heartbeat, network logs) are suspicious.
- Compare the host's audit policy (`auditpol /get /category:*` or `Policy\PolAdtEv` in SECURITY hive) with the GPO baseline.

## Gotchas
- GPO refresh may restore audit policy, leaving only a short gap - 4719 events bracket it.
- Event forwarding (WEF/agent) failures look like gaps too; check the forwarder's health before concluding tampering.

## Verify
Each gap or change is tied to an actor/process or explained as an infrastructure fault.
