---
id: computing-software.cybersecurity-defensive.security-operations.kql-hunting-queries
name: kql-hunting-queries
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, kql-hunting, kql, threat-hunting, advanced-hunting, bookmarks, defender-xdr]
level: practitioner
status: docs-checked
description: "Hunt in Microsoft Sentinel and Defender XDR with KQL: query patterns, joins and time windows, hunting queries, bookmarks and hunts."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/hunting", "https://learn.microsoft.com/en-us/kusto/query/", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# KQL hunting queries

**Goal:** write fast, correct KQL to test a hunting hypothesis and keep the evidence.

## Query shape
Filter early, on time first, then on indexed columns, then project:
```
DeviceProcessEvents
| where Timestamp > ago(7d)
| where FileName in~ ("rundll32.exe","regsvr32.exe")
| where ProcessCommandLine has_any ("http","\\\\","javascript:")
| project Timestamp, DeviceName, AccountName, ProcessCommandLine, InitiatingProcessFileName
```
- `has` searches indexed terms (three or more characters) and is case-insensitive; `has_any`
  takes a list of terms. `in~` is the case-insensitive form of `in`.
- `summarize ... by bin(TimeGenerated, 1h)` for trends; `make-series` + `series_decompose_anomalies()`
  for anomaly detection.

## Correlate
```
let suspicious = SigninLogs
| where TimeGenerated > ago(1d) and RiskLevelDuringSignIn == "high"
| project UserPrincipalName, SigninTime=TimeGenerated, IPAddress;
OfficeActivity
| where TimeGenerated > ago(1d) and Operation contains "InboxRule"
| join kind=inner suspicious on $left.UserId == $right.UserPrincipalName
| where TimeGenerated between (SigninTime .. SigninTime + 2h)
```
Put the smaller table on the left of `join`; the default `innerunique` dedupes the left side,
so say `kind=inner` when you mean it.

## Rare and first-seen
```
DeviceNetworkEvents | where Timestamp > ago(30d)
| summarize Devices=dcount(DeviceId), First=min(Timestamp) by RemoteUrl
| where Devices <= 2 and First > ago(1d)
```

## Sentinel hunting workflow
- Save useful queries as hunting queries and use the Run all queries button (or a subset)
  to see how they apply to your environment.
- Bookmark interesting rows and escalate them to an incident. Bookmarks are in Sentinel >
  Threat management > Hunting; they are not available in Advanced hunting.
- Livestream is no longer available; automate queries and notifications with KQL jobs,
  analytics rules or playbooks.
- Hunts track a hypothesis, the queries and the results together.

## Gotchas
- Advanced hunting covers up to 30 days of native Defender XDR data; longer retention needs a
  Sentinel workspace with the table retention configured.
- Column names differ: `Timestamp` in Defender XDR tables, `TimeGenerated` in Azure Monitor and Sentinel tables.
- Aggregate in KQL instead of exporting raw rows.

## Verify
Re-run the query over a known incident's timeframe and confirm it returns the known-bad
activity; record hit counts before converting to a rule.

## Checked
2026-10-28 Confirmed on the Kusto and Microsoft Learn pages: `has` and `has_any` behaviour, `in~`, join kinds (`innerunique` default, smaller table on the left), `make-series` and `series_decompose_anomalies`, table and column names (DeviceProcessEvents/DeviceNetworkEvents fields, SigninLogs `RiskLevelDuringSignIn`, OfficeActivity `UserId` as UPN), the 30-day advanced hunting range, Run all queries, bookmarks, hunts. Fixed: livestream is no longer available per the Sentinel hunting page. Removed: the `contains` scan claim, `=~`/`startswith` advice, exact Exchange operation names, menu paths and result size limits (not on the fetched pages).
Method: documentation only; no commands were run.
