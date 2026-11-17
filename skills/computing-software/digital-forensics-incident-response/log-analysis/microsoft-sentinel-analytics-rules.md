---
id: computing-software.digital-forensics-incident-response.log-analysis.microsoft-sentinel-analytics-rules
name: microsoft-sentinel-analytics-rules
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sentinel-analytics-rules, microsoft-sentinel, kql, detection-engineering, scheduled-rules, dfir]
level: practitioner
status: docs-checked
description: "Build Microsoft Sentinel scheduled and NRT analytics rules: query schedule and lookback, threshold, event grouping, entity mapping, incident grouping, suppression, testing."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/create-analytics-rules", "https://learn.microsoft.com/en-us/azure/sentinel/near-real-time-rules", "https://learn.microsoft.com/en-us/azure/sentinel/map-data-fields-to-entities"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft Sentinel analytics rules

Analytics rules turn KQL queries over Log Analytics tables into alerts and incidents. During and after an incident they are how you make findings durable detections.

## Rule types covered here
- **Scheduled query rule**: runs your KQL on a schedule over a lookback window. Created from Analytics, then +Create, then Scheduled query rule.
- **NRT (near-real-time) rule**: hard-coded to run once every minute over events ingested in the preceding minute, using ingestion time instead of `TimeGenerated`, with a two-minute delay (scheduled rules have a built-in five-minute delay). Limits: no more than 50 NRT rules per customer, works properly only on log sources with ingestion delay under 12 hours, and it can produce up to 30 single-event alerts (a query with more than 30 events yields alerts for the first 29 plus a 30th that summarises all of them). NRT rules support entity mapping, custom details, alert details, incident grouping, suppression and automation.

## Scheduled rule settings that matter
| Setting | What the documentation says |
|---|---|
| Query | Must return `TimeGenerated`, which is the reference for the lookback; only records inside the lookback window are evaluated. Build and test it in Logs first. |
| Run query every | 5 minutes to 14 days |
| Lookup data from the last | 5 minutes to 14 days, and must be longer than or equal to the query interval |
| Alert threshold | "Generate alert when number of query results is greater than" a number; enter 0 for no threshold |
| Event grouping | "Group all events into a single alert" (default) or "Trigger an alert for each event" |
| Suppression | "Stop running query after alert is generated" with a stop duration of up to 24 hours |
| Entity mapping | Up to 10 entity mappings per rule; the same entity type can be mapped more than once (for example a source and a destination IP). Up to 500 entities per alert, split equally across mappings; the Entities field is limited to 64 KB |
| Custom details / alert details | Surface query fields in alerts and incidents; customise alert name or description from field values |
| Severity and MITRE ATT&CK | Choose severity by the impact if the alert is a true positive, and map tactics and techniques (multiple allowed) |
| Incident settings | "Create incidents from alerts" is Enabled by default (leave it Enabled if onboarded to the Defender portal, where Defender XDR creates incidents) |
| Alert grouping | Group alerts into one incident within a chosen time frame by all entities matching (recommended), by all alerts of the rule, or by matching entities plus selected details; up to 150 alerts per incident, excess goes into a new incident; "Re-open closed matching incidents" is not available in the Defender portal |
| Automation | Automated response tab lists automation rules; add new ones there. Playbooks can no longer be added under "Alert automation (classic)" |

## Workflow
1. Design the query in Logs and confirm the table name from the data connector page.
2. Fill in the wizard: general information, rule logic, incident settings, automated response.
3. Use "Test with current data" in Results simulation: Sentinel simulates running the rule 50 times on current data and graphs the results.
4. To manage rules as code, export the rule to an ARM template and import it elsewhere (Import and export analytics rules).

## Verify
A test event produces the expected incident with mapped entities, and the rule's schedule, lookback and threshold match the intended detection.

## Checked
Checked 2026-11-09 against the Microsoft Learn pages "Create a scheduled analytics rule", "Near-real-time (NRT) analytics rules" and "Map data fields to entities" (settings, ranges, limits, defaults). Removed: the Fusion, Anomaly, Threat Intelligence and Microsoft security rule-type descriptions, the "1 h over 1 h 10 m" lookback example, the SecurityEvent KQL example, the 14-30 day testing advice, Atomic Red Team, `SentinelHealth` and auto-disable notes, and the watchlist and cross-workspace timeout gotchas, none of which the cited pages state in that form. The `detect-threats-custom` source was a redirect to the same article and was dropped.
Method: documentation only; no commands were run.
