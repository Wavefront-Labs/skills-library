---
id: computing-software.systems-network-administration.windows-server.sysmon-deployment-and-configuration
name: sysmon-deployment-and-configuration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-auditing, sysmon, sysinternals, event-forwarding, threat-detection]
level: practitioner
status: docs-checked
description: "Deploy Sysmon on Windows servers with a tuned XML config, update it safely, read key events (1, 3, 7, 10, 11, 22) and forward them for detection."
sources:
  - https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
  - https://github.com/SwiftOnSecurity/sysmon-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon deployment and configuration

Sysmon (Sysinternals) is a driver + service that logs process, network, file and registry activity to
`Microsoft-Windows-Sysmon/Operational`.

## Install with a config
```cmd
sysmon64.exe -accepteula -i sysmonconfig.xml
sysmon64.exe -c sysmonconfig.xml        REM update config in place
sysmon64.exe -c                         REM show current config
sysmon64.exe -u                         REM uninstall
```
A community baseline such as SwiftOnSecurity's sysmon-config (see sources) is a common starting point; tune it for your software.

## Fleet deployment
- Keep the config in source control; review changes like code.
- Forward the Sysmon log to your SIEM (for example with Windows Event Forwarding).

## Key events
| ID | Event |
|---|---|
| 1 | process create (command line, hashes, parent) |
| 3 | network connection |
| 7 | image loaded (DLL) - noisy, filter tightly |
| 8 | CreateRemoteThread |
| 10 | process access |
| 11 | file create |
| 12/13 | registry create/set |
| 22 | DNS query |
| 25 | process tampering |
| 4 / 16 | Sysmon state / config changed (alert on these) |

## Verify
- [ ] Event 1 appears for a test process with command line and hash; SIEM receives Sysmon events from every server.

## Checked

2026-10-28. Confirmed against: Sysmon page (install/update/uninstall switches -i, -c, -u, -accepteula, event log path, event IDs 1, 3, 4, 7, 8, 10, 11, 12, 13, 16, 22, 25) and the SwiftOnSecurity sysmon-config readme. Removed (not confirmable from the cited pages): comparison with event 4688, sysmon-modular reference, GPO/ConfigMgr deployment steps, log size figures, EDR altitude and service-stop (7036) statements, schema-version note.

Method: documentation only; no commands were run.
