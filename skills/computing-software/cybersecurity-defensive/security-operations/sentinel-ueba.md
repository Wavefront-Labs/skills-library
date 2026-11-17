---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-ueba
name: sentinel-ueba
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-ueba, ueba, behavioranalytics, identityinfo, entity-pages, anomalies, insider-threat, kql]
level: practitioner
status: docs-checked
description: "Enable and use Sentinel UEBA: data sources, BehaviorAnalytics and IdentityInfo tables, investigation priority scores, entity pages, and using UEBA in rules."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/identify-threats-with-entity-behavior-analytics", "https://learn.microsoft.com/en-us/azure/sentinel/enable-entity-behavior-analytics", "https://learn.microsoft.com/en-us/azure/sentinel/ueba-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel UEBA

UEBA builds per-user and per-peer-group baselines and writes enriched, scored events. It is
context for investigations and a signal for rules, not an alerting engine on its own.

## Enable
Sentinel > Settings > Entity behavior analytics:
1. Directory service: Microsoft Entra ID (and on-prem AD via Defender for Identity if present).
2. Data sources: SigninLogs, AuditLogs, AzureActivity, SecurityEvent (4624/4625 etc.),
   and others offered for your connectors. Only selected sources are profiled.
3. Baselines need a period of history before scores are meaningful.

## Tables
- `BehaviorAnalytics`: one row per enriched activity with `ActivityInsights` (first time
  user connected from country, uncommon ISP, first time action performed), `UsersInsights`,
  `DevicesInsights`, and `InvestigationPriority` (0-10).
- `IdentityInfo`: synced identity attributes (department, manager, groups, assigned roles,
  account status) - the best join table for enriching any alert.
- `UserPeerAnalytics`: peer group membership and rank.
- `Anomalies`: output of Sentinel anomaly rules (ML templates in Analytics > Anomalies).

## Hunting with UEBA
```
BehaviorAnalytics
| where TimeGenerated > ago(7d) and InvestigationPriority >= 5
| extend FirstCountry = tostring(ActivityInsights.FirstTimeUserConnectedFromCountry)
| project TimeGenerated, UserPrincipalName, ActivityType, ActionType, SourceIPAddress,
          SourceIPLocation, FirstCountry, InvestigationPriority
| order by InvestigationPriority desc
```
Enrich alerts with identity context by joining `IdentityInfo` on the account (take the latest row per account with `arg_max`).

## Entity pages
Incident > entity > View full details: timeline of alerts, activities, and UEBA insights; use it
as the first stop for "is this normal for this user?" during triage.

## Gotchas
- Scope UEBA data sources deliberately; check the Sentinel billing documentation for the cost of the UEBA tables.
- New users and service accounts have no baseline: everything is "first time".
- Anomaly rules are noisy; use them as risk inputs or hunting leads, not incident creators.

## Checked
2026-10-28. Confirmed in the UEBA reference and entity behavior analytics pages: `BehaviorAnalytics` with `InvestigationPriority` (0-10), `UserPeerAnalytics`, `Anomalies`, `IdentityInfo`. Removed: the 2-3 week baseline figure, the untested enrichment join, and the billing claim.
Method: documentation only; no commands were run.

## Verify
`BehaviorAnalytics | summarize count() by bin(TimeGenerated,1d), ActionType` shows daily rows for
each enabled source, and `IdentityInfo | take 10` returns current users.
