---
id: computing-software.digital-forensics-incident-response.log-analysis.defender-advanced-hunting-tables
name: defender-advanced-hunting-tables
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [advanced-hunting, microsoft-defender-xdr, kql, deviceprocessevents, identitylogonevents, emailevents, edr, dfir]
level: practitioner
status: gated
description: "Investigate with Microsoft Defender XDR advanced hunting: key Device, Identity, Email and Cloud app tables, KQL patterns, joins, retention and limits."
sources: ["https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-best-practices"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Defender advanced hunting tables

**Goal:** query Microsoft Defender XDR telemetry quickly and correctly during an investigation.

## Key tables
| Table | Content |
|---|---|
| `DeviceProcessEvents` | process creation: `FileName`, `ProcessCommandLine`, `InitiatingProcess*` (parent), `AccountName`, hashes |
| `DeviceNetworkEvents` | connections: `RemoteIP`, `RemoteUrl`, `RemotePort`, `ActionType` (ConnectionSuccess, InboundConnectionAccepted) |
| `DeviceFileEvents` | file create/modify/delete/rename with `FolderPath`, `SHA256`, `FileOriginUrl` |
| `DeviceRegistryEvents` | registry changes |
| `DeviceLogonEvents` | logons to devices (`LogonType`, `RemoteIP`) |
| `DeviceImageLoadEvents` | DLL loads |
| `DeviceEvents` | many `ActionType`s: AMSI, `PowerShellCommand`, `NamedPipeEvent`, `DnsQueryResponse`, exploit guard, `LdapSearch` |
| `DeviceInfo`, `DeviceNetworkInfo`, `DeviceTvmSoftwareInventory` | asset context |
| `IdentityLogonEvents`, `IdentityQueryEvents`, `IdentityDirectoryEvents` | Defender for Identity (AD/DC): logons, LDAP/SAMR queries, group changes |
| `EmailEvents`, `EmailAttachmentInfo`, `EmailUrlInfo`, `UrlClickEvents` | Defender for Office 365 |
| `CloudAppEvents` | Defender for Cloud Apps / M365 activity |
| `AADSignInEventsBeta` / `EntraIdSignInEvents` | Entra sign-ins (naming evolving) |
| `AlertInfo`, `AlertEvidence` | alerts and their entities |

## KQL patterns
```kusto
// Process tree context for a suspicious command line
DeviceProcessEvents
| where Timestamp between (datetime(2026-09-14 08:00) .. datetime(2026-09-14 12:00))
| where DeviceName =~ "ws042.corp.local"
| where ProcessCommandLine has_any ("-enc", "FromBase64String", "rundll32", "comsvcs")
| project Timestamp, AccountName, InitiatingProcessFileName, InitiatingProcessCommandLine, FileName, ProcessCommandLine, SHA256

// Who clicked a phishing URL and what ran afterwards
UrlClickEvents | where Url has "evil.example" | project ClickTime=Timestamp, AccountUpn, Url
| join kind=inner (DeviceProcessEvents | project Timestamp, DeviceName, AccountUpn=InitiatingProcessAccountUpn, ProcessCommandLine) on AccountUpn
| where Timestamp between (ClickTime .. ClickTime + 30m)

// Hash prevalence across the estate
DeviceFileEvents | where SHA256 == "<hash>" | summarize dcount(DeviceId), min(Timestamp), max(Timestamp)
```

## Limits to remember
- Retention: 30 days of native Defender XDR data; onboard a Microsoft Sentinel workspace and configure
  analytics-tier retention to keep tables longer.
- Query limits (overview page): 100,000 rows per query, 10 minute timeout, 64 MB result size, and CPU
  quotas per tenant refreshed every 15 minutes. Filter on `Timestamp` and device first, use `has` over
  `contains`, project early.
- Absence of an event is not proof it did not happen; note retention limits in conclusions.
- Custom detections can be created directly from a hunting query (Create detection rule).

## Self-check
Your queries are time-bounded, scoped to entities, saved in the case notes, and you noted
retention or sampling limits affecting conclusions.

## Checked

- Date: 2026-11-02.
- Confirmed against: table names DeviceProcessEvents, DeviceFileEvents, UrlClickEvents and column names ProcessCommandLine, InitiatingProcessFileName (Defender advanced hunting overview, schema tables and best-practices pages).
- Not confirmed: columns like AccountUpn and LogonType and the less common tables (PowerShellCommand, NamedPipeEvent, DnsQueryResponse, LdapSearch), which the fetched schema page does not list (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
