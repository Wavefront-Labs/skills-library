---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-analytics-rules
name: sentinel-analytics-rules
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-analytics-rules, scheduled-rules, nrt-rules, kql, entity-mapping, alert-grouping, detection-engineering]
level: advanced
status: docs-checked
description: "Write Microsoft Sentinel scheduled and NRT analytics rules: query windows, entity mapping, alert grouping into incidents, suppression and deployment as code."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/create-analytics-rules", "https://learn.microsoft.com/en-us/azure/sentinel/near-real-time-rules", "https://learn.microsoft.com/en-us/azure/sentinel/map-data-fields-to-entities"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel scheduled and NRT analytics rules

**Goal:** detections that fire once per real incident, carry entities for investigation,
and never miss events between runs.

## Scheduled rule settings that matter
- **Query frequency** and **lookback**: lookback must be at least frequency plus ingestion
  delay. Deduplicate overlapping results.
- Scheduled rules use `TimeGenerated` as the reference for the lookback window: the query must return that column, and only records whose `TimeGenerated` falls inside the lookback are evaluated. Size the lookback to allow for ingestion delay.
- **Threshold:** generate alert when results > 0, or a count threshold.
- **Event grouping:** one alert per result (per-entity) vs one alert for all results.

## Entity mapping
Map columns to Account (UPN, ObjectGuid), Host, IP, URL, FileHash, Process. Entities drive
the investigation graph, UEBA, and incident correlation. Use `custom details` for extra
fields an analyst needs on the incident card, and `alert details` to put the user and host
in the alert name dynamically.

## Incident settings
Group alerts into incidents by matching entities within a window (same Account, for example)
so a burst of alerts becomes one incident; reopen closed incidents on new matches only
if that fits your workflow.

## NRT rules
Run every minute with a one-minute lookback (not configurable); queries can reference more than one table but have KQL restrictions. Use for a few high-value signals (break-glass
account sign-in, audit log cleared). Do not convert everything to NRT.

## Suppression and tuning
- "Stop running query after alert is generated" for up to 24 hours avoids repeats.
- Prefer allowlists in a watchlist joined in the query over editing the KQL each time.
- Automation rules can close known benign patterns, with a comment for audit.

## As code
Export rules as ARM/Bicep or YAML (Sentinel repository format) and deploy via Sentinel
Repositories (GitHub/Azure DevOps). Store the rule id GUID stably so updates replace rather
than duplicate.

## Gotchas
- Rules created from Content hub templates can diverge from the template; review template updates before accepting them.
- Rule queries are subject to result limits and query timeouts; summarise in KQL.
- Disabled due to repeated failures: check Health (SentinelHealth table).

## Checked
2026-10-28. Confirmed in the Sentinel create analytics rules, NRT rules and health monitoring pages: scheduled rules use `TimeGenerated` for the lookback; NRT rules run each minute with a one-minute lookback and can reference more than one table; "Stop running query" up to 24 hours; `_SentinelHealth()` with `SentinelResourceType` and auto-disabled rules. Corrected: the `ingestion_time()` advice and the NRT single-table claim. Removed: lookback figures, 5 h grouping window, 10,000 result limit, alert-name placeholder example, template update wording.
Method: documentation only; no commands were run.

## Verify
```
_SentinelHealth() | where SentinelResourceType == "Analytics Rule" and Status != "Success"
SecurityAlert | where TimeGenerated > ago(7d) | summarize count() by AlertName | sort by count_ desc
```
