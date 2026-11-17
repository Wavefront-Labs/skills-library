---
id: computing-software.cybersecurity-defensive.security-operations.edr-telemetry-investigations
name: edr-telemetry-investigations
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [edr-telemetry, investigation-data-sources, defender-for-endpoint, crowdstrike, advanced-hunting, process-tree, kql]
level: practitioner
status: draft
description: "Use EDR telemetry for investigations: process trees, network and file events, Defender Advanced Hunting and CrowdStrike Event Search queries, retention limits and gaps."
sources: ["https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables", "https://falcon.crowdstrike.com/documentation/", "https://www.elastic.co/guide/en/security/current/endpoint-event-capture.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# EDR telemetry for investigations

## What EDR records (and does not)
- Process creation with command line, parent, user, integrity, hashes, signer.
- Network connections (process-attributed), DNS (some), file create/modify/delete (often filtered
  to interesting paths/types), registry, image loads, logons, script content (AMSI).
- Not everything: high-volume events are sampled or filtered; file reads are rarely recorded;
  retention typically 30 days (Defender) to 7-90 days (varies by licence).

## Defender for Endpoint (KQL)
```kql
DeviceProcessEvents
| where DeviceName == "ws-123" and Timestamp between (datetime(2026-10-17 09:00) .. 2h)
| project Timestamp, FileName, ProcessCommandLine, InitiatingProcessFileName, InitiatingProcessCommandLine, AccountName, SHA256
DeviceNetworkEvents | where InitiatingProcessFileName =~ "rundll32.exe" and RemoteIPType == "Public"
DeviceFileEvents | where FolderPath has @"\ProgramData\" and ActionType == "FileCreated"
```
Tables: DeviceProcessEvents, DeviceNetworkEvents, DeviceFileEvents, DeviceRegistryEvents,
DeviceImageLoadEvents, DeviceLogonEvents, DeviceEvents (AMSI, exploit guard, etc.).

## CrowdStrike Falcon
Event Search / Advanced Event Search (LogScale): `#event_simpleName=ProcessRollup2 ComputerName=ws-123`
joined to `NetworkConnectIP4` by `ContextProcessId` = `TargetProcessId`; `DnsRequest`; process
tree in the detection graph.

## Workflow
1. Start from the alert process; walk up parents to origin (email client, browser, service,
   remote logon) and down to children.
2. Pivot on hashes/command lines across the fleet for other hosts.
3. Collect artefacts EDR lacks (full memory, $MFT, browser history) via live response.

## Gotchas
- Process ID reuse: join on unique process IDs (Defender `InitiatingProcessId` + creation time;
  Falcon `TargetProcessId`), not PID alone.
- Device time vs ingestion time; use event time.
- Tamper protection off or sensor offline creates silent gaps; check sensor health timeline.

## Verify
Investigation timeline cites EDR event IDs/time for each step and notes any retention or sensor gaps.
