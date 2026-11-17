---
id: computing-software.cybersecurity-defensive.endpoint-security.defender-advanced-hunting
name: defender-advanced-hunting
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [edr, advanced-hunting, kql, microsoft-defender-xdr, threat-hunting, custom-detection-rules]
level: advanced
status: draft
description: "Hunt in Microsoft Defender XDR advanced hunting with KQL: key Device tables, efficient query patterns, joins across process and network events, and promoting hunts to custom detections."
sources: ["Microsoft Learn - Advanced hunting overview and schema reference", "Microsoft Learn - Advanced hunting query best practices", "Microsoft Learn - Create and manage custom detection rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defender advanced hunting

**Goal:** fast, accurate KQL hunts across endpoint telemetry, turned into scheduled detections when they prove useful.

## Key tables
`DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `DeviceRegistryEvents`, `DeviceLogonEvents`, `DeviceImageLoadEvents`, `DeviceEvents` (misc incl. ASR, AMSI), `DeviceInfo`, plus `EmailEvents`, `IdentityLogonEvents`, `CloudAppEvents`, `AlertInfo`/`AlertEvidence`. Retention 30 days in advanced hunting (longer via Sentinel).

## Query patterns
Encoded PowerShell launched by Office:
```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where InitiatingProcessFileName in~ ("winword.exe","excel.exe","outlook.exe")
| where FileName in~ ("powershell.exe","pwsh.exe","cmd.exe","mshta.exe","rundll32.exe")
| project Timestamp, DeviceName, AccountName, InitiatingProcessFileName, FileName, ProcessCommandLine
```
Process + network join (rare outbound by LOLBIN):
```kql
DeviceNetworkEvents
| where Timestamp > ago(3d) and RemoteIPType == "Public"
| where InitiatingProcessFileName in~ ("rundll32.exe","regsvr32.exe","mshta.exe","certutil.exe")
| summarize Conns=count(), Hosts=dcount(DeviceId) by RemoteUrl, InitiatingProcessFileName
| where Hosts < 3
```
Stacking (rare autoruns):
```kql
DeviceRegistryEvents
| where RegistryKey has @"\CurrentVersion\Run" and ActionType == "RegistryValueSet"
| summarize Devices=dcount(DeviceId), Sample=any(RegistryValueData) by RegistryValueName
| where Devices <= 2
```

## Performance
Filter on `Timestamp` first, then on indexed-like columns (`FileName`, `ActionType`), use `has` over `contains`, `in~` for lists, project only needed columns before `join`, put the smaller table on the left of joins. Queries time out at a few minutes and results cap at 100,000 rows (10,000 in portal display).

## Custom detections
From a working query: "Create detection rule"; must return `Timestamp`, `DeviceId` and `ReportId` (from the same event); set frequency (every hour to 24 h, or continuous/NRT for supported queries), impacted entities, and automated actions (isolate, collect investigation package) cautiously.

## Verify
- [ ] Hunt queries saved in shared queries with description and ATT&CK technique.
- [ ] Each custom detection tested with an Atomic Red Team or benign trigger.
