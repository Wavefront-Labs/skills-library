---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-workbooks
name: sentinel-workbooks
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-workbooks, siem-dashboards, azure-monitor-workbooks, kql, parameters, soc-reporting]
level: practitioner
status: docs-checked
description: "Build Sentinel workbooks for SOC reporting: parameters, time range and workspace pickers, query steps, drill-through links, cross-workspace queries, and saving as templates."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/monitor-your-data", "https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview", "https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-parameters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel workbooks

Workbooks are Azure Monitor workbooks: a sequence of steps (parameters, queries, text, links)
rendered as a report. Use them for SOC metrics, data-source health and investigation views.

## Start
Sentinel > Workbooks > Templates (Content hub solutions add many) > Save to get an editable copy,
or Add workbook for a blank one. Edit mode exposes each step's settings.

## Parameters
- **Time range** parameter (`TimeRange`) and use `{TimeRange}` in queries' time picker setting.
- **Workspace** parameter (resource picker, multi-select) for MSSP or multi-workspace views.
- **Drop-down from query**: fill a parameter's values from a KQL query and reference it by name in later steps (see the workbooks parameters page for the syntax).
- Text parameters for free filters, with "Required" unticked and the query written to cope with an empty value.

## Query steps
Each query step runs KQL against the workspace; use the time range parameter for the time filter. Look up each table's columns in the Azure Monitor table reference before relying on them.
- Visualisations: grid with heatmap/threshold formatting, time chart, tiles, map, graph.

## Performance and cost
- Every step runs a query each time the workbook loads; limit time ranges by default (24h/7d).
- Use summarised tables or Summary rules for heavy historic views.

## Sharing
Saved workbooks live as Azure resources in a resource group; RBAC controls who can view.
Viewers also need read access to the workspace tables queried (resource-context or table RBAC).
For version control, Advanced editor > Gallery template JSON and keep it in the content repo.

## Verify
Load with each parameter combination, compare a tile value with the same KQL run in Logs, and
check the workbook loads acceptably for the default range.

## Checked

Date: 2026-10-28

- Confirmed in the Learn pages fetched: workbooks are Azure Monitor workbooks built from parameters, queries and links; saving a template; deleting workbooks leaves templates; Content hub and summary-rule references.
- Removed (not found in the fetched pages): the sample KQL and the SecurityIncident column names, the {RuleName}/{User} parameter examples, Column settings and export-parameter UI labels, the cross-workspace query form and the 10 second load target.
Method: documentation only; no commands were run.
