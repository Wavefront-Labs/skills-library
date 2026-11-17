---
id: computing-software.cloud-infrastructure-engineering.azure.resource-graph-queries-in-log-alerts-and-workbooks
name: resource-graph-queries-in-log-alerts-and-workbooks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-graph, arg-alerts, arg-workbooks, log-search-alerts, cross-service-query, governance-alerting]
level: advanced
status: docs-checked
description: "Alert on and visualise Azure inventory: arg() cross-service queries in log search alerts with a managed identity, ARG data sources in workbooks."
sources: ["https://learn.microsoft.com/azure/azure-monitor/logs/azure-monitor-data-explorer-proxy", "https://learn.microsoft.com/azure/governance/resource-graph/alerts-query-quickstart", "https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-data-sources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource Graph in alerts and workbooks

**Goal:** get alerted when the estate drifts (public IPs appear, VMs stop heartbeating) and see it on dashboards.

## Log search alerts using arg()
Log Analytics can query Resource Graph with `arg("").<table>`; the feature is in public preview. Table names are case-insensitive in practice (`Resources` or `resources`).
```kusto
arg("").Resources
| where type == 'microsoft.compute/virtualmachines'
| project ResourceId = id, name, PowerState = tostring(properties.extended.instanceView.powerState.code)
| join (Heartbeat
  | where TimeGenerated > ago(15m)
  | summarize lastHeartBeat = max(TimeGenerated) by ResourceId)
  on ResourceId
| project lastHeartBeat, PowerState, name, ResourceId
```
(This is the Learn quickstart query: VMs with a recent heartbeat; alert with operator Less than and a threshold sized to your fleet.)

Alert rule setup (portal, from the workspace Logs blade, New alert rule):
- Scope: the Log Analytics workspace. Signal: Custom log search; measure Table rows, aggregation Count.
- Details tab, Identity: **System assigned managed identity**. The fired alert runs as that identity, so a manual run (your identity) can return a different count.
- Assign **Log Analytics Reader** to the alert rule's identity (rule > Settings > Identity > Azure role assignments), at the subscription in the quickstart. For Azure Data Explorer clusters add Reader on the cluster.
- A new configuration can take 30 minutes before monitoring data is queryable.

## Cross-service query limits (documented)
- The `arg` part returns only the first 1,000 records; with a join, rows can go missing if the limit is hit.
- `join` takes one ARG table and one Log Analytics table, and needs `hint.remote=<direction of the workspace>`; `union` also works (`union AzureActivity, arg("").Resources`).
- Azure Monitor does not return ARG query errors, and the Log Analytics editor may flag valid ARG queries as syntax errors.
- Cross-service functions must not be parameterised or contain other cross-workspace expressions.

## Workbooks
Query step > Query type **Azure Resource Graph** > scope level (Subscriptions, Management groups or the whole Tenant) > select targets > write the Resource Graph KQL (a KQL subset, no `arg("")` wrapper). Use the merge control to combine ARG results with Log Analytics or metrics data.

## Verify
- [ ] Sandbox test resource triggers the alert in an evaluation period; the alert identity shows Log Analytics Reader.

## Checked
2026-10-31. Confirmed on the alerts quickstart, data-explorer-proxy and workbooks-data-sources Learn pages: preview status, arg("") syntax, the sample query, system-assigned identity step, Log Analytics Reader role, 1,000-record limit, join hint, workbook ARG query type and scope levels. Removed: the Reader-on-management-group claim (page uses Log Analytics Reader), the `az monitor scheduled-query create --mi-system-assigned` example (flag not on the CLI reference), the orphan public IP query (unsourced), ARG lag and "sub-minute" claims, the Grafana and dashboards line.
Method: documentation only; no commands were run.
