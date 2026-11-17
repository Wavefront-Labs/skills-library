---
id: computing-software.cloud-infrastructure-engineering.azure.diagnostic-settings-resource-logs-and-activity-log
name: diagnostic-settings-resource-logs-and-activity-log
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, diagnostic-settings, resource-logs, activity-log, platform-logs, platform-metrics, log-categories, category-groups, alllogs, audit, resource-specific-tables, azurediagnostics, log-destinations, event-hub-export, storage-archive, policy-deploy-diagnostics, entra-diagnostic-settings, audit-logs, signin-logs, azureactivity, retention]
level: practitioner
status: docs-checked
description: "Turn on platform logs: diagnostic settings with category groups to Log Analytics, Storage or Event Hubs, Activity log and Entra ID export, deployed by Policy."
sources: ["https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings", "https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log", "https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings-policy", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-configure-diagnostic-settings", "https://learn.microsoft.com/en-us/cli/azure/monitor/diagnostic-settings/subscription"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnostic settings — platform logs on for everything, by policy, without the bill shock

**Goal:** every resource that can emit logs does, into the right workspace, with only the
categories you need, and the control plane (Activity log, Entra) captured centrally for the auditors.

## 1. What a diagnostic setting is
Create a separate setting per resource. Each setting picks **categories** (resource logs such as
`AuditEvent`) or a **category group** (`allLogs` = every category, `audit` = logs that record customer
interaction with data or settings; not every service offers groups, and with a group you cannot also pick
single categories), optional **platform metrics** (`AllMetrics`), and destinations: Log Analytics
(query/alert), Storage (archive; send to immutable storage to prevent modification), Event Hubs (stream to a
SIEM), Azure Monitor partner solutions.
- Platform metrics and the Activity log are collected automatically; **resource logs are not collected by default**.
- Each resource can have up to **5** settings; one setting holds at most one destination of each type.
- The destination must already exist. For regional resources, Storage accounts and Event Hubs must be in the same region.
  With virtual networks enabled, allow trusted Microsoft services to bypass the firewall on the Storage account or Event Hubs.
  Premium Storage accounts are not supported; any Standard account is.
- Event Hubs: a compacted event hub cannot be used; streaming needs Manage, Send and Listen permissions on the namespace policy, and `ListKey` on the authorization rule to update a setting.
- Delete a resource's settings before deleting, renaming or moving it; otherwise a re-created resource can pick up the old setting.
- Data should flow within 90 minutes of creating a setting; the Log Analytics table is created on the first record.
```bash
az monitor diagnostic-settings categories list --resource <kv-id>      # what this type can emit
az monitor diagnostic-settings create --resource <kv-id> -n to-law --workspace <law-id> --export-to-resource-specific true \
  --logs '[{"categoryGroup":"audit","enabled":true}]' --metrics '[{"category":"AllMetrics","enabled":true}]'
```
- `--export-to-resource-specific true` selects resource-specific mode (dedicated tables) where the service supports it.
- Metric categories other than `AllMetrics` are rejected for most services ("Metric category is not supported").
- Diagnostic settings do not support resource IDs containing non-ASCII characters.

## 2. Control cost by choosing categories
Collect only the categories each service needs. Settings cost nothing themselves; destinations bill by volume (see the Azure Monitor pricing page).
Skip `AllMetrics` to a workspace unless you need metrics in log queries: platform metrics are already in metrics explorer. Diagnostic settings cannot filter inside a category; use a transformation on the workspace table for that.
Enabling the `audit` group for Azure SQL Database does not turn on SQL auditing; enable that on the database's auditing pane.

## 3. Activity log (control plane)
Azure keeps Activity log events for **90 days** with no ingestion charge. To keep them longer, export with a **subscription-scope** setting (the resource-scope `create` is not for the Activity log):
```bash
az monitor diagnostic-settings subscription create -n activity-to-law --location <region> --workspace <law-id> \
  --logs '[{"category":"Administrative","enabled":true},{"category":"Security","enabled":true},{"category":"ServiceHealth","enabled":true},{"category":"Alert","enabled":true},{"category":"Recommendation","enabled":true},{"category":"Policy","enabled":true},{"category":"Autoscale","enabled":true},{"category":"ResourceHealth","enabled":true}]'
```
In a workspace the data lands in the `AzureActivity` table; retention charges apply only beyond 90 days, up to 12 years. Compare strings in `AzureActivity` case-insensitively (`=~`). Send to a Storage account for retention beyond 90 days for audit.
A management-group setting exports that group and the groups under it, but events without the ARM `hierarchy` property do not propagate; keep a subscription-level setting too, and note that overlapping settings to the same destination produce duplicates.

## 4. Entra ID logs (tenant)
Entra admin centre → Entra ID → Monitoring & health → Diagnostic settings (Security Administrator at least). Choose log categories, then Log Analytics, Event Hubs, Storage or a partner. Create the destination first; logs can take up to three days to appear. Keep custom security attribute audit logs in a separate setting (Attribute Log Administrator role).

## 5. Scale with Policy
Use Azure Policy initiatives of `DeployIfNotExists` definitions (built-in per resource type, or custom where none exists) assigned at a management group, subscription or resource group. Use initiative parameters for the workspace or Event Hub, give the assignment a managed identity with a role such as Monitoring Contributor or Log Analytics Contributor, and create a remediation task for existing resources (new resources are handled at creation). The built-in definitions expose `allLogs` and `audit` variants.

## Gotchas
- A setting for a Storage account or Event Hubs namespace cannot use that same resource as destination in the portal (CLI/ARM can).
- Application Insights: the destination cannot be the workspace the component is based on.
- A resource with inactive zero-value metrics backs off its export (up to 15 minutes, max after seven days of inactivity).
- Cross-subscription destinations need RBAC on both; use Lighthouse for another Entra tenant.

## Verify
- [ ] `az monitor diagnostic-settings list --resource <id>` shows the categories you expect enabled.
- [ ] A test event appears in the workspace table (allow up to 90 minutes after creating the setting).
- [ ] `AzureActivity | where TimeGenerated > ago(1h)` returns rows for every production subscription.

## Checked
2026-10-28. Confirmed on the Diagnostic settings in Azure Monitor, Activity log, diagnostic settings at scale with Policy, Entra diagnostic settings and `az monitor diagnostic-settings subscription` pages: five settings per resource, one destination type per setting, destination constraints, category groups, 90-minute latency, 90-day Activity log retention with no ingestion charge and up to 12 years, `AzureActivity`, subscription-scope CLI export and category list, management-group behaviour, Entra path and roles, Policy initiative/remediation/managed identity. Removed: per-service category table, resource-specific table names, Entra sign-in table list and P1/P2 and 30-day retention claims, Event Hubs partition sizing and hub naming, policy compliance percentages, Lighthouse and workspace-deletion remarks, and the Bicep pattern advice.
Method: documentation only; no commands were run.
