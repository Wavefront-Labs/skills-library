---
id: computing-software.cloud-infrastructure-engineering.azure.dcr-xpath-filtering-for-windows-events
name: dcr-xpath-filtering-for-windows-events
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor-agent, xpath-queries, event-filtering-xpath, data-collection-rules, windows-event-logs]
level: advanced
status: docs-checked
description: "Write and test XPath queries in data collection rules to collect only needed Windows events with AMA, validate them with Get-WinEvent and control ingestion cost."
sources: ["https://learn.microsoft.com/azure/azure-monitor/agents/data-collection-windows-events", "https://learn.microsoft.com/windows/win32/wes/consuming-events", "https://learn.microsoft.com/azure/azure-monitor/agents/data-collection-rule-azure-monitor-agent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XPath filtering of Windows events in DCRs

**Goal:** collect exactly the Windows events you need with Azure Monitor Agent instead of whole channels.

## Format
DCR `windowsEventLogs` data source uses `ChannelName!XPathQuery`:
```json
"dataSources": { "windowsEventLogs": [ {
  "name": "secAndSys", "streams": [ "Microsoft-Event" ],
  "xPathQueries": [
    "System!*[System[(Level=1 or Level=2 or Level=3)]]",
    "Security!*[System[(EventID=4624 or EventID=4625 or EventID=4740)]]",
    "Microsoft-Windows-Windows Defender/Operational!*[System[(EventID=1116 or EventID=1117)]]"
  ] } ] }
```
The `Microsoft-Event` stream is the standard stream for Windows event logs.

## Useful patterns
- By provider: `Application!*[System[Provider[@Name='MSSQLSERVER']]]`
- Exclude noise: `Security!*[System[(EventID=4624)]] and *[EventData[Data[@Name='LogonType']!='3']]`

## Test before deploying
```powershell
$x = "*[System[(EventID=4624 or EventID=4625)]]"
Get-WinEvent -LogName Security -FilterXPath $x -MaxEvents 5
```
Test the XPath on a machine before adding it to a DCR.

## Limits and gotchas
- Windows event log XPath is limited (XPath 1.0 limitations): functions such as `starts-with` and `contains` are not supported.
- Channel names with spaces and slashes are used as-is in `ChannelName!XPath`.
- Filtering at the agent with XPath reduces what is sent to the workspace; see Learn for how it compares with ingestion-time transformations.

## Verify
- [ ] `Event | where TimeGenerated > ago(1h) | summarize count() by EventLog, EventID` shows only intended IDs.
- [ ] `az monitor data-collection rule show -g rg -n dcr1 --query dataSources.windowsEventLogs` matches the repo.

## Checked

Date: 2026-10-28.

Confirmed against Learn (DCR structure, collect Windows events with AMA): `windowsEventLogs` data source with `xPathQueries`, stream `Microsoft-Event`, the Windows event log XPath 1.0 limitations (`starts-with` and `contains` unsupported).
Removed: the `Microsoft-SecurityEvent` stream claim, no-time-filter claim, Get-WinEvent/AMA equivalence, query complexity limit, the 50% transformation charge and `transformKql` detail (not on fetched pages).

Method: documentation only; no commands were run.
