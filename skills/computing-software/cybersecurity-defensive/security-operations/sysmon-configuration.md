---
id: computing-software.cybersecurity-defensive.security-operations.sysmon-configuration
name: sysmon-configuration
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, sysmon-config, sysmon, sysinternals, event-id-1, event-id-3, event-id-10, swiftonsecurity, olafhartong-sysmon-modular, endpoint-telemetry]
level: practitioner
status: draft
description: "Deploy Sysmon with a maintained config (sysmon-modular / SwiftOnSecurity), tune noisy events, and know which event IDs answer which investigation question."
sources: ["Microsoft Sysinternals - Sysmon documentation", "olafhartong/sysmon-modular (GitHub)", "SwiftOnSecurity/sysmon-config (GitHub)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sysmon configuration and events

**Goal:** rich process, network and file telemetry on Windows hosts at an event volume the
SIEM can afford, especially where no EDR telemetry reaches the SIEM.

## Deploy
```
Sysmon64.exe -accepteula -i sysmonconfig.xml     # install
Sysmon64.exe -c sysmonconfig.xml                 # update config
Sysmon64.exe -s                                  # print schema
```
Push via GPO/Intune/SCCM. Events go to `Microsoft-Windows-Sysmon/Operational`; collect with
your forwarder (Splunk TA for Sysmon, AMA/DCR in Sentinel, Elastic Agent Windows integration).

## Start from a maintained config
- **sysmon-modular** (Olaf Hartong): modules mapped to ATT&CK, merge to one file, variants for verbosity.
- **SwiftOnSecurity sysmon-config**: well-commented baseline, good starting point.
Keep the config in Git and change it through review.

## Event IDs you rely on
| ID | Event | Use |
|---|---|---|
| 1 | Process create (hashes, command line, parent) | Execution chains |
| 3 | Network connect | Process-to-network attribution (noisy: filter) |
| 7 | Image loaded | DLL side-loading (very noisy: include-only rules) |
| 8 | CreateRemoteThread | Injection |
| 10 | ProcessAccess | Credential dumping (`TargetImage` lsass.exe with suspicious `GrantedAccess`) |
| 11 | File create | Dropped payloads |
| 12/13/14 | Registry events | Run keys and other persistence |
| 22 | DNS query | Process-level DNS |
| 23/26 | File delete (archived / logged) | Evidence destruction, ransomware |
| 25 | Process tampering | Hollowing/herpaderping |

## Tuning
- Exclude by exact `Image` path plus signer where possible, never by process name alone
  (an attacker names their binary `chrome.exe`).
- Measure events per host per day by ID after rollout; aim for a predictable budget (often
  a few thousand per workstation per day, more on servers).
- `HashAlgorithms` SHA256 plus IMPHASH is a good balance; more algorithms cost CPU.

## Gotchas
- A config error rejects the whole update; validate with `-c` on a test host first.
- Event ID 7 and 3 without filters can multiply volume by 10x.
- Sysmon does not log command output or script contents: pair with PowerShell script block logging.
- Attackers check for and unload Sysmon (`fltMC unload SysmonDrv`): alert on the driver unload and on gaps in the event stream.

## Verify
- [ ] `Get-WinEvent -LogName Microsoft-Windows-Sysmon/Operational -MaxEvents 5` returns events on a sample host.
- [ ] Config version is visible (`Sysmon64 -c` prints the hash) and matches Git.
- [ ] A test (`whoami /all` from a cmd spawned by Word in a lab) produces event 1 with the full chain.
