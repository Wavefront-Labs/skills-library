---
id: computing-software.cybersecurity-defensive.splunk.sentinel-incident-investigation
name: sentinel-incident-investigation
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [microsoft-sentinel, sentinel-incident-investigation, investigation-graph, entity-pages, kql, incident-management, bookmarks]
level: practitioner
status: docs-checked
description: "Investigate Microsoft Sentinel incidents: incident page, entities and timeline, investigation graph, entity pages, bookmarks and closing with classification."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/investigate-incidents", "https://learn.microsoft.com/en-us/azure/sentinel/investigate-cases", "https://learn.microsoft.com/en-us/azure/sentinel/entity-pages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sentinel incident investigation

## Incident page
- Header: severity, status, owner, tactics, linked alerts. Assign yourself and set the status first. The Microsoft Sentinel Responder role is required to investigate incidents.
- **Timeline**: alerts and bookmarks in time order; **Entities** tab: accounts, hosts, IPs, files,
  URLs extracted by analytics rule entity mapping. Poor entity mapping makes this empty; fix the rule.

## Investigate
- Open each entity page: activity timeline, insights (first-time logon from country, rare process),
  related alerts across workspaces you can read.
- Investigation graph (Investigate button): expand entities with exploration queries; good for showing blast radius visually.
- Run KQL from the Logs blade; pivot on `SecurityAlert`, `SigninLogs`, `DeviceProcessEvents`.
  Example:
```kql
SigninLogs
| where UserPrincipalName =~ "user@example.com" and TimeGenerated > ago(7d)
| summarize count() by IPAddress, Location, ResultType, AppDisplayName
```
- Save evidence rows as **bookmarks** and add them to the incident; they appear on the timeline.
- Add comments for each decision; comments are the audit trail.

## Close
Close the incident with a classification and a comment; the options are in the close dialog and are stored in `Classification`, `ClassificationReason` and `ClassificationComment` of `SecurityIncident`. Feed false positives back into the rule (automation rule exclusions or KQL tuning).

## Gotchas
- Investigation graph requires entities mapped with identifiers; display names only won't expand.

## Verify
Closed incident has owner, classification, comments explaining the decision, and bookmarks for
every key piece of evidence.

## Checked

Date: 2026-10-28

- Confirmed: Responder role needed to investigate incidents, incident entities come from analytics rule entity mapping, investigation graph requires entities, entity page timelines include alerts and bookmarks, SecurityIncident Classification/ClassificationReason/ClassificationComment columns, SigninLogs columns (UserPrincipalName, IPAddress, Location, ResultType, AppDisplayName).
- Removed (not found): time-to-acknowledge metric claim, similar-incident 14-day window, UEBA insight bullets, named exploration queries, the closing classification list, Defender merge/close behaviour.
Method: documentation only; no commands were run.

