---
id: computing-software.digital-forensics-incident-response.incident-response-process.hunting-ransomware-precursors
name: hunting-ransomware-precursors
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ransomware-precursors, ransomware, threat-hunting, cobalt-strike, data-exfiltration, dfir]
level: advanced
status: draft
description: "Hunt for pre-encryption ransomware activity: initial loaders, Cobalt Strike, AD recon, credential dumping, rclone exfil and defence tampering."
sources: ["https://www.cisa.gov/stopransomware/ransomware-guide", "https://thedfirreport.com/", "https://attack.mitre.org/tactics/TA0040/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hunting ransomware precursors

**Goal:** ransomware is the last step of an intrusion that typically runs days to weeks. Finding
the precursors stops encryption, and after an encryption event identifies the full scope.

## Precursor categories and what to hunt
| Phase | Typical tools / artefacts | Where |
|---|---|---|
| Initial access | IcedID/QakBot/Pikabot successors, exposed VPN/RDP, ISO/LNK lures | EDR, proxy, VPN logs |
| C2 | Cobalt Strike, Brute Ratel, Sliver beacons; named pipes like `\\.\pipe\MSSE-*-server` | Sysmon 17/18, memory, JA3/JA4 |
| Discovery | AdFind, `nltest /domain_trusts`, `net group "domain admins" /domain`, SharpHound, Advanced IP Scanner | 4688/Sysmon 1, prefetch |
| Credential access | LSASS dumps (comsvcs MiniDump, procdump), NTDS via `ntdsutil ifm`, Mimikatz | Sysmon 10, 4662, file creation |
| Lateral movement | PsExec, WMI, RDP with new admin accounts, RMM tools (AnyDesk) | 7045, 4624 type 3/10 |
| Exfiltration | rclone (often renamed) with `config` to MEGA/S3, WinSCP, FileZilla | process command lines, proxy volume |
| Defence evasion | Defender exclusions, `Set-MpPreference -DisableRealtimeMonitoring`, GMER/PCHunter, BYOVD | Defender 5001/5007, 7045 |
| Pre-impact | `vssadmin delete shadows`, `wbadmin delete catalog`, `bcdedit /set recoveryenabled no`, GPO deployment | 4688, 5136 |

## Hunting technique
- Stack process names and command lines for the tools above across the fleet; rclone renamed
  shows up by its flags (`--transfers`, `copy`, `--config`).
- Look for new admin accounts and new GPOs in the last 30 days.
- Check large outbound transfers to cloud storage ASNs from servers.

## Gotchas
- Legitimate admins use AdFind/Advanced IP Scanner; context (account, time, host) decides.
- After encryption, precursors on encrypted hosts may only survive in EDR telemetry or backups.

## Verify
Each hit is attributed (admin vs attacker) and attacker hits are pivoted to timeline and scope.
