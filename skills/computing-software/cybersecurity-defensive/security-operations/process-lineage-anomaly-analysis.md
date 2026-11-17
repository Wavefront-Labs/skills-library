---
id: computing-software.cybersecurity-defensive.security-operations.process-lineage-anomaly-analysis
name: process-lineage-anomaly-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [process-lineage-analysis, threat-hunting, process-tree, parent-child-relationships, edr-telemetry, sysmon, stack-counting]
level: practitioner
status: draft
description: "Analyse process lineage for anomalies: unusual parent-child pairs, rare grandparent chains, office and browser children, service-spawned shells, with stack counting."
sources: ["https://www.sans.org/posters/hunt-evil/", "https://attack.mitre.org/techniques/T1059/", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Process lineage anomaly analysis

## Known-good references
SANS "Hunt Evil": `smss.exe` -> `wininit.exe`/`csrss.exe`; `services.exe` parent of `svchost.exe`;
`lsass.exe` child of `wininit.exe`; `explorer.exe` from `userinit.exe`. Any deviation (e.g.
`svchost.exe` not started by `services.exe`, `lsass.exe` in wrong path) is suspicious.

## Stack-count parent/child pairs
```kql
DeviceProcessEvents
| where Timestamp > ago(14d)
| summarize hosts=dcount(DeviceId), n=count() by InitiatingProcessFileName, FileName
| where hosts <= 3
| order by hosts asc
```
Review the long tail: rare pairs across the fleet.

## High-value patterns
- Office apps (`winword.exe`, `excel.exe`, `outlook.exe`) spawning scripting engines,
  `mshta.exe`, `rundll32.exe`, `regsvr32.exe`.
- Browsers spawning shells (except known helpers).
- `wmiprvse.exe` spawning `powershell.exe` (WMI lateral movement), `services.exe` spawning
  `cmd.exe` with random service names (PsExec-like).
- `sqlservr.exe`, `w3wp.exe`, `java.exe` spawning shells (exploitation).
- Scheduled task host (`svchost.exe -k netsvcs -p -s Schedule`) children from user-writable paths.

## Grandparent context
Add `InitiatingProcessParentFileName` to distinguish legitimate chains (e.g. `explorer -> cmd ->
powershell` by admin) from `outlook -> cmd -> powershell`.

## Linux
`sshd -> bash` normal; `nginx/apache/java -> sh` suspicious; `cron -> curl | sh`.

## Gotchas
- PPID spoofing (T1134.004) fakes parents; EDRs record the creator process separately; use it.
- Software installers and management agents create many rare pairs; build allowlists by signer
  and path.

## Verify
Hunt output: reviewed rare pairs with verdicts, allowlist updates, and detections for confirmed patterns.
