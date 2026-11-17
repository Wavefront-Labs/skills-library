---
id: computing-software.cloud-infrastructure-engineering.azure.sentinel-ueba-and-entity-behavior-analytics
name: sentinel-ueba-and-entity-behavior-analytics
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, sentinel, microsoft-sentinel, ueba, entity-behavior, behavioranalytics, identityinfo, entity-pages, anomalies, investigation-priority, peer-analysis, insider-risk, hunting]
level: advanced
status: docs-checked
description: "Enable and use Microsoft Sentinel UEBA: data sources, BehaviorAnalytics and IdentityInfo tables, investigation priority, entity pages and anomaly rules in detection and hunting."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/identify-threats-with-entity-behavior-analytics", "https://learn.microsoft.com/en-us/azure/sentinel/enable-entity-behavior-analytics", "https://learn.microsoft.com/en-us/azure/sentinel/ueba-reference", "https://learn.microsoft.com/en-us/azure/sentinel/investigate-with-ueba"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel UEBA — entity behaviour analytics

**Goal:** baselines of normal behaviour for users and hosts so analysts see "this is unusual for
this user and their peers" in every incident, and hunting can pivot on anomaly scores.

## 1. Enable
Sentinel → *Settings → Entity behavior analytics* (or Defender portal → Settings → Microsoft Sentinel):
1. **Directory service**: Microsoft Entra ID (and/or on-prem Active Directory via Defender for Identity) — populates `IdentityInfo`.
2. **Data sources** for behaviour: select them in the UEBA settings; the supported list is on the UEBA reference page.
3. Also enable **Anomalies** (Analytics → *Anomalies* templates) — ML rules writing to the `Anomalies` table.
Baselines need time to build before scores are meaningful.

## 2. Tables
| Table | Content |
|---|---|
| `BehaviorAnalytics` | enriched events with `ActivityInsights` (first time user did X, uncommon among peers), `UsersInsights`, `DevicesInsights`, `InvestigationPriority` (0–10) |
| `IdentityInfo` | user attributes: department, manager, groups, assigned roles, `BlastRadius`, risk state |
| `UserPeerAnalytics` | peer groups computed from group membership/org |
| `Anomalies` | output of anomaly rules |
```kusto
BehaviorAnalytics
| where TimeGenerated > ago(1d) and InvestigationPriority >= 5
| project TimeGenerated, UserPrincipalName, ActivityType, ActionType, SourceIPLocation, InvestigationPriority,
          FirstTimeAction=tostring(ActivityInsights.FirstTimeUserPerformedAction),
          UncommonAmongPeers=tostring(ActivityInsights.ActionUncommonlyPerformedAmongPeers)
| order by InvestigationPriority desc
```
```kusto
// enrich any detection with org context and blast radius
SigninLogs | where ResultType == 0 | join kind=inner (IdentityInfo | summarize arg_max(TimeGenerated,*) by AccountUPN) on $left.UserPrincipalName == $right.AccountUPN
| where AssignedRoles has "Global Administrator" and RiskLevelDuringSignIn != "none"
```

## 3. Use in operations
- **Entity pages** (user/host/IP): timeline of alerts, anomalies and activities, insights panels — the analyst's starting point from any incident.
- Add `InvestigationPriority`/`BlastRadius` to analytics rules to raise severity for privileged or high-anomaly users; use anomaly matches as a *second signal* rather than standalone alerts.
- Hunting: queries over `Anomalies` and high-priority `BehaviorAnalytics` rows → bookmarks → incidents.

## Gotchas
- Without on-prem AD sync, hybrid identities miss attributes; enable both directory sources where relevant.
- Insights rely on the data sources selected; turning on UEBA without `SigninLogs` gives empty baselines.

## Verify
- [ ] UEBA settings show directory and data sources enabled; `IdentityInfo` populated for all users.
- [ ] `BehaviorAnalytics` has rows with non-zero `InvestigationPriority` after the learning period.
- [ ] Entity page for a test user displays insights; at least one analytics rule uses UEBA enrichment.

## Checked
2026-10-28. Confirmed on the UEBA reference and investigation pages: `InvestigationPriority` is an int score 0-10, `BlastRadius` derived from org position and Entra roles (Low/Medium/High), anomalies shown on user entity pages for the last 30 days, `IdentityInfo` and `BehaviorAnalytics` tables. Removed as unconfirmed: the 1-3 week baseline, enabling roles, data source list, Anomalies columns, Purview, cost and Flighting claims. The KQL samples use column names not individually verified.
Method: documentation only; no commands were run.
