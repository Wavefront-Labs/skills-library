---
id: computing-software.cloud-infrastructure-engineering.azure.application-insights-classic-to-workspace-based-migration
name: application-insights-classic-to-workspace-based-migration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-insights, workspace-based-application-insights, classic-ai-migration, log-analytics, connection-string]
level: practitioner
status: docs-checked
description: "Migrate classic Application Insights resources to workspace-based: impact on queries, tables, retention, cost, continuous export replacement and the connection string switch."
sources: ["https://learn.microsoft.com/azure/azure-monitor/app/convert-classic-resource", "https://learn.microsoft.com/azure/azure-monitor/app/create-workspace-resource", "https://learn.microsoft.com/azure/azure-monitor/app/sdk-connection-string"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classic to workspace-based Application Insights

**Goal:** move off classic Application Insights without losing data or breaking queries and alerts. Microsoft began phased automatic migration in May 2024 but strongly encourages manual migration (start from the retirement banner on the classic resource's Overview).

## What changes
- Telemetry is stored in a Log Analytics workspace in tables `AppRequests`, `AppDependencies`, `AppExceptions`, `AppTraces`, `AppPageViews`, `AppMetrics` (was customMetrics), `AppEvents` (was customEvents), `AppAvailabilityResults`, `AppBrowserTimings`, `AppPerformanceCounters`.
- Queries against the workspace must use the new table names; most columns keep their name with different capitalisation, and KQL is case sensitive (for example `duration` becomes `DurationMs`).
- New data follows the workspace's retention and billing. Data already in the classic resource keeps the classic retention settings.
- Migration causes no downtime or restart and does not change the instrumentation key or connection string.

## Migrate
```bash
az monitor app-insights component update --app appi1 -g rg --workspace <workspaceResourceId>
```
Migration is permanent and cannot be reversed (you can change the target workspace afterwards). The target workspace needs access control mode "Use resource or workspace permissions".

## Follow-ups
- **Continuous export** is not compatible with workspace-based resources and must be disabled before migrating; use **diagnostic settings** (storage account or Event Hubs) afterwards. The export schema differs, which breaks existing Azure Stream Analytics integrations.
- Rewrite saved queries, alerts and workbooks that use classic table or column names.
- Check retention: if you keep data longer than the default 90 days, adjust the workspace retention.
- After migration use the workspace daily cap instead of the Application Insights cap.
- With Terraform, use azurerm provider 3.89 or higher before migrating.

## Verify
- [ ] The resource Overview shows a linked workspace and the classic retirement banner is gone.
- [ ] `AppRequests | where _ResourceId has "appi1" | take 5` in the workspace returns new data.

## Checked
2026-10-28. Confirmed in Learn convert-classic-resource: phased migration from May 2024, table name mapping (including AppBrowserTimings and
AppPerformanceCounters), column casing, permanent migration, no downtime or key change, retention behaviour, continuous export
and diagnostic settings, daily cap, Terraform 3.89, access control mode, and the `az monitor app-insights component update --workspace`
command. Removed: the 29 Feb 2024 retirement date, the `TimeGenerated`/`ResultCode` column claims, cross-resource app() advice,
commitment-tier wording, the portal blade path, and the ingestionMode CLI check.
Method: documentation only; no commands were run.
