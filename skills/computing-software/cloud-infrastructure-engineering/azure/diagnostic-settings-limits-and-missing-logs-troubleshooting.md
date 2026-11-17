---
id: computing-software.cloud-infrastructure-engineering.azure.diagnostic-settings-limits-and-missing-logs-troubleshooting
name: diagnostic-settings-limits-and-missing-logs-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, diagnostic-settings, diagnostic-settings-limits, missing-logs, log-analytics, resource-logs]
level: practitioner
status: docs-checked
description: "Troubleshoot resource logs that do not arrive: diagnostic setting limits, category coverage, destination type, latency, Azure Policy DINE gaps and permission issues."
sources: ["https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostic-settings", "https://learn.microsoft.com/azure/azure-monitor/essentials/resource-logs", "https://learn.microsoft.com/azure/azure-monitor/logs/data-ingestion-time", "https://learn.microsoft.com/azure/azure-monitor/essentials/diagnostic-settings-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnostic settings limits and missing logs

**Goal:** find out quickly why a resource's logs are not in Log Analytics.

## Limits and rules
- Each resource can have up to **5 diagnostic settings**.
- Not every service supports every category; check `az monitor diagnostic-settings categories list --resource <id>`.

## Checklist when logs are missing
1. **Setting exists and is enabled**: `az monitor diagnostic-settings list --resource <id> -o table`. Category group `allLogs` vs specific categories.
2. **Right table**: resource-specific tables versus `AzureDiagnostics` (the destination table setting decides). Query the right one.
3. **Latency**: varies by destination and service (see Learn: Log data ingestion time in Azure Monitor). Check `ingestion_time() - TimeGenerated`.
4. **Workspace side**: daily cap reached (check `_LogOperation`), workspace in a different tenant without Azure Lighthouse, table plan changes, a data collection transformation filtering rows.
5. **Activity happened**: resource logs only exist when the resource does something (no requests = no access logs).
6. **Policy-deployed settings**: the policy initiative applies on resource creation; existing resources need a remediation task. Policy settings may target a different workspace.
7. **Permissions**: you need rights to write the diagnostic setting on the resource and to the destination; check the RBAC requirements on the diagnostic settings page.

```kusto
_LogOperation | where TimeGenerated > ago(1d) | summarize count() by Category, Operation, Detail
AzureDiagnostics | where ResourceId =~ "<id>" | summarize max(TimeGenerated) by Category
```

## Verify
- [ ] Recent record for each expected category: `union withsource=T * | where _ResourceId =~ "<id>" | summarize max(TimeGenerated) by T`.

## Checked

Date: 2026-10-28.

Confirmed against Learn (diagnostic-settings, resource-logs, diagnostic-settings-policy, data-ingestion-time): five settings per resource, allLogs category group, ingestion latency varies by destination, policy remediation task for existing resources, resource-specific versus AzureDiagnostics tables. CLI commands via check_commands.py.
Removed: one-destination-per-type and duplicate-category rules, subscription-level activity log claim, table names, 30 s to 3 min latency figures, the _LogOperation filter, exact permission strings and the storage/Event Hub firewall and throttling claims.

Method: documentation only; no commands were run.
