---
id: computing-software.cybersecurity-defensive.splunk.sentinel-health-and-audit-monitoring
name: sentinel-health-and-audit-monitoring
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [microsoft-sentinel, sentinel-health-monitoring, sentinelhealth, sentinelaudit, data-connector-health, kql, log-source-health]
level: practitioner
status: docs-checked
description: "Monitor Microsoft Sentinel health and auditing with SentinelHealth and SentinelAudit tables: connector failures, analytics rule failures, automation errors and alerts on them."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/health-audit", "https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring", "https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sentinel health and audit monitoring

## Enable
Sentinel > Settings > Settings > Auditing and health monitoring > Enable. Choose data connectors,
analytics rules, automation (and audit). Tables: `SentinelHealth`, `SentinelAudit`.

## Queries
Analytics rule failures and delays:
```kql
SentinelHealth
| where SentinelResourceType == "AlertRule" and Status != "Success"
| summarize failures=count(), last=max(TimeGenerated) by SentinelResourceName, Status, Description
```
Connector failures (only supported connectors report; see the health-audit page for the list):
```kql
SentinelHealth
| where SentinelResourceType == "DataConnector" and Status == "Failure"
| project TimeGenerated, SentinelResourceName, Reason, Description
```
Automation and playbook failures: SentinelHealth records automation rule runs; Logic App actions are in the AzureDiagnostics table.

Audit changes to rules (who disabled a detection):
```kql
SentinelAudit
| where SentinelResourceType == "AlertRule"
| where Description has "Delete" or Description has "Update"
| project TimeGenerated, SentinelResourceName, Status, ExtendedProperties
```

## Ingestion health beyond SentinelHealth
Many connectors are not covered; check silence per table:
```kql
union withsource=T *
| where TimeGenerated > ago(1d)
| summarize last=max(TimeGenerated) by T
| where last < ago(2h)
```
Use the **Data collection health monitoring** workbook for volume anomalies.

## Alerting
Turn the failure queries into scheduled analytics rules, or Azure Monitor alerts, routed to the platform team.

## Gotchas
- Only supported resources report health; no records for a resource means check coverage, not assume healthy.

## Verify
Break a test connector (revoke its secret) or rule (reference a missing table); confirm the alert
fires within the expected window.

## Checked

Date: 2026-10-28

- Confirmed: SentinelHealth and SentinelAudit tables, enabling auditing and health monitoring in Settings, columns Status, Reason, Description, SentinelResourceName, ExtendedProperties (Azure Monitor table reference), Status values Success, Failure, Warning, Informational, Partial Success, automation health combines SentinelHealth with AzureDiagnostics.
- Corrected: SentinelResourceType examples are DataConnector and AlertRule (not display names). Removed: connector list, auto-disable claim, health event cadence claim, specific rule severities.
Method: documentation only; no commands were run.

