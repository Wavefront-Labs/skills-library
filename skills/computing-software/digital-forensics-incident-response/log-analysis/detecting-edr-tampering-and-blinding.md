---
id: computing-software.digital-forensics-incident-response.log-analysis.detecting-edr-tampering-and-blinding
name: detecting-edr-tampering-and-blinding
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [edr-tampering, edr, anti-forensics, byovd, dfir]
level: advanced
status: draft
description: "Detect EDR tampering: agent stops and uninstalls, sensor heartbeat gaps, tamper-protection alerts, BYOVD killers, network blocking of sensor traffic and safe-mode abuse."
sources: ["https://attack.mitre.org/techniques/T1562/001/", "https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection", "https://www.loldrivers.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting EDR tampering and blinding

**Goal:** attackers disable or blind EDR before ransomware or data theft (ATT&CK T1562.001). The
absence of telemetry is the signal - if you look for it.

## Techniques and signals
| Technique | Signals |
|---|---|
| Stop/uninstall agent with admin rights or uninstall token | Agent "uninstalled"/"offline" in console; Windows 7036/7040 service stop/disable; MSI uninstall events 1034/11724 |
| Tamper protection attempts | EDR tamper alerts; Defender 5013 (tamper protection blocked a change), 5001/5007 |
| BYOVD process killers (EDRKillShifter, AuKill, Terminator) | 7045 kernel driver service creation; Sysmon 6; vulnerable driver hashes (loldrivers) |
| Safe mode reboot (`bcdedit /set {default} safeboot minimal`) | bcdedit command lines; boot into safe mode where agent is not running (events 12/13 with safe boot) |
| Blocking sensor cloud traffic (Windows Firewall rules, hosts file, WFP filters like EDRSilencer) | Agent online locally but no telemetry; new firewall rules (event 2004/2097 in Firewall log), hosts file modification; WFP filter changes (5441/5447) |
| Unhooking / direct syscalls / ETW patching in process | EDR-specific alerts; memory analysis showing patched ntdll |
| Deleting agent files/logs | File deletions under agent directories |

## Fleet-level detection
- **Heartbeat gap monitoring**: list hosts whose sensor last-seen is older than N minutes while the host is
  still active in other sources (DHCP, AD logons, firewall logs). Alert on it.
- Compare agent inventory with CMDB/AD computer list daily; investigate newly unmanaged hosts.
- SIEM rule for service stop/uninstall of security products by name, and for `sc config <edr> start= disabled`.

## Response
- Treat confirmed tampering on a host as hands-on-keyboard activity: escalate severity, isolate via network (since the agent may not respond), collect memory/disk.
- Enable tamper protection, uninstall passwords/tokens, and vulnerable driver blocklist fleet-wide.

## Gotchas
- Legitimate upgrades and IT troubleshooting stop agents; correlate with change tickets.
- When the EDR is blind, its console shows nothing - pivot to network, AD and other logs for the period.

## Verify
Every heartbeat gap during the incident window is explained, and tampered hosts are identified with the method used.
