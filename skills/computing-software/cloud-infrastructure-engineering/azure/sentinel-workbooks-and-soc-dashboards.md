---
id: computing-software.cloud-infrastructure-engineering.azure.sentinel-workbooks-and-soc-dashboards
name: sentinel-workbooks-and-soc-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, microsoft-sentinel, sentinel-workbooks, soc-dashboards, content-hub, kql]
level: practitioner
status: gated
description: "Deploy and build Microsoft Sentinel workbooks for SOC dashboards: content hub templates, parameters, KQL visualisations, sharing, and workbooks as code."
sources: ["https://learn.microsoft.com/azure/sentinel/monitor-your-data", "https://learn.microsoft.com/azure/sentinel/sentinel-solutions-deploy", "https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-overview", "https://learn.microsoft.com/azure/sentinel/manage-soc-with-incident-metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel workbooks and SOC dashboards

**Goal:** dashboards the SOC actually uses: data health, incident metrics, threat views.

## Start from templates
- **Content hub**: install solutions that ship workbook templates. Sentinel → Workbooks → Templates → *Save* creates an editable copy in the workspace.

## Build custom panels
- Parameters: time range, subscription/workspace multi-select, severity drop-down.
- Example tile: incidents by severity and status over time (gated: unconfirmed, source is paywalled or blocked) (column names of SecurityIncident not confirmed):
```kusto
SecurityIncident
| where TimeGenerated {TimeRange}
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| summarize count() by Severity, Status, bin(CreatedTime, 1d)
| render columnchart
```
- MTTR:
```kusto
SecurityIncident | summarize arg_max(TimeGenerated,*) by IncidentNumber
| where Status == "Closed" | extend ttc = datetime_diff('minute', ClosedTime, CreatedTime)
| summarize avg(ttc), percentile(ttc, 90) by Severity
```
- Use grids with links to incidents (`IncidentUrl`), heatmaps for sign-in failures by location, and conditional visibility for drill-down.

## Sharing and access
- Saved workbooks are Azure resources in a resource group; viewers also need read access to the workspace data. Check the Azure Monitor workbooks documentation for the exact roles.

## As code
- Export the workbook JSON (Advanced editor) and deploy it with ARM or Bicep; see the workbooks documentation for the resource schema.

## Verify
- [ ] SOC lead reviews workbook weekly; queries return in acceptable time for the ranges used.

## Checked

2026-10-28. Confirmed on the Sentinel incident metrics page: the IncidentUrl field exists in the incident metrics schema. Removed: named solutions and template list, the resource picker type, role names, the workbook resource type and serializedData property, the repositories feature claim and the 30-day timing. Gated: the two SecurityIncident KQL examples (table columns such as ClosedTime and CreatedTime not confirmed in fetched pages).

Method: documentation only; no commands were run.
