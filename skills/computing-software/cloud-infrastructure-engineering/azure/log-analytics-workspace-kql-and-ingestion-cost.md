---
id: computing-software.cloud-infrastructure-engineering.azure.log-analytics-workspace-kql-and-ingestion-cost
name: log-analytics-workspace-kql-and-ingestion-cost
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, log-analytics, log-analytics-workspace, kql, kusto, log-queries, workspace-design, commitment-tiers, basic-logs, auxiliary-logs, analytics-logs, log-retention, archive, search-jobs, ingestion-transformations, dcr-transformations, ingestion-cost, usage-table, data-export, workbooks, resource-context-access, table-level-rbac, summary-rules, workspace-replication]
level: practitioner
status: draft
description: "Run Log Analytics well: workspace topology and access mode, table plans and retention, commitment tiers, DCR transformations to cut noise, Usage-table cost analysis, and ops KQL patterns."
sources: ["Microsoft Learn - Design a Log Analytics workspace architecture", "Microsoft Learn - Azure Monitor Logs table plans (Analytics, Basic, Auxiliary) and retention", "Microsoft Learn - Analyze usage in Log Analytics workspace and reduce costs", "Microsoft Learn - Data collection transformations in Azure Monitor", "Microsoft Learn - KQL quick reference and Azure Monitor log query examples"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log Analytics — one workspace you can afford, queries you can trust

**Goal:** a workspace layout that matches your tenancy, every table on the cheapest
plan that still serves its purpose, ingestion you can explain line by line, and a KQL
toolkit for incidents.

## 1. Workspace topology
- Default: **one workspace per region per environment class** (prod / non-prod) in the
  management subscription; Sentinel in the same workspace as security logs. Split only for
  data sovereignty, separate retention/plans, or hard tenant isolation. Cross-workspace
  queries (`workspace("law-eu").Heartbeat`) and **workspace replication** (cross-region DR) exist.
- Access mode: **resource-context** (workspace property `features.enableLogAccessUsingOnlyResourcePermissions`, set via portal *Properties* or ARM) lets app teams query logs for resources they can read via `Resource > Logs`, without workspace RBAC. Table-level RBAC (`Microsoft.OperationalInsights/workspaces/tables/<T>/read`) for sensitive tables (`SecurityEvent`, `SigninLogs`).
```bash
az monitor log-analytics workspace create -g rg-mon -n law-prod-uks -l uksouth --retention-time 90 --sku PerGB2018 --quota 50   # daily cap GB (safety net; stops Sentinel security data too — exempt via Sentinel settings)
az monitor log-analytics workspace update ... --sku CapacityReservation --capacity-reservation-level 100   # commitment tier when > ~100 GB/day (≈15-30 % cheaper)
```

## 2. Table plans and retention
| Plan | Use | Cost model |
|---|---|---|
| **Analytics** (default) | anything you alert/dashboard on | per GB ingest; 31 days interactive free (90 for App Insights/Sentinel), then retention charge; up to 2 years interactive, 12 years total with archive |
| **Basic** | high-volume debug/verbose logs queried rarely (`ContainerLogV2`, `AppTraces`, custom) | ~¼ ingest price, 30-day interactive, limited KQL (single-table queries with lookups only), queries billed per GB scanned |
| **Auxiliary** | compliance firehose (firewall/flow logs you must keep) | lowest ingest, query via search jobs only |
```bash
az monitor log-analytics workspace table update -g rg-mon --workspace-name law-prod-uks -n ContainerLogV2 --plan Basic
az monitor log-analytics workspace table update ... -n SecurityEvent --retention-time 180 --total-retention-time 730   # interactive 180d, archive to 2y
```
Search jobs (`az monitor log-analytics workspace table search-job create --search-query "..." --start-time ... --end-time ...`)
pull archived/Auxiliary data into a new `_SRCH` table; restore (`table restore create`) brings a range back interactive.

## 3. Find what you pay for
```kusto
Usage | where TimeGenerated > ago(30d) and IsBillable
| summarize GB=sum(Quantity)/1024 by DataType | order by GB desc        // by table
Usage | where IsBillable | summarize GB=sum(Quantity)/1024 by bin(TimeGenerated,1d), Solution | render columnchart
find where TimeGenerated > ago(1d) project _ResourceId, _BilledSize | summarize GB=sum(_BilledSize)/1e9 by _ResourceId | top 20 by GB   // by resource
AzureDiagnostics | summarize GB=sum(_BilledSize)/1e9 by ResourceType, Category | order by GB desc   // the usual culprits
```
Typical fixes: AKS `ContainerLogV2` → Basic + collect only needed namespaces (ConfigMap
`container-azm-ms-agentconfig`); `AzureDiagnostics` for Firewall/AGW → resource-specific
tables; `Perf` counters every 60 s → 300 s via DCR; `Syslog` facility/level filtering;
App Insights sampling; Windows `SecurityEvent` tier *Common* not *All*. The *Workspace Insights*
and *Usage and estimated costs* blades show the same with a cost projection.

## 4. Transformations (drop before you pay)
In the DCR (`transformKql` on the data flow, or a workspace default DCR for tables fed by diagnostic settings):
```kusto
source | where SeverityLevel != "Verbose" | where not(Computer startswith "build-") | project-away RawData
```
- Can filter rows, drop columns, mask (`replace_regex`), add computed columns, and split
  to multiple tables. Filtered-out data isn't billed (beyond a small processing charge once
  > 50 % is dropped).
- Workspace transformation DCR applies to resource logs/Activity log sent via diagnostic settings — the only way to trim `AzureDiagnostics` before ingest.
- Summary rules (`az monitor log-analytics workspace ...` / portal) aggregate a verbose table into a small `_CL` table on a schedule — keep raw in Basic, alert on the summary.

## 5. KQL for incidents (keep in a shared query pack)
```kusto
// who logged into what, failed
SigninLogs | where ResultType != 0 | summarize n=count(), apps=make_set(AppDisplayName,5) by UserPrincipalName, ResultDescription | top 20 by n
// VM heartbeat gaps
Heartbeat | summarize last=max(TimeGenerated) by Computer, _ResourceId | where last < ago(10m)
// 5xx by app with p95 latency
AppRequests | where TimeGenerated > ago(1h) | summarize req=count(), err=countif(Success == false), p95=percentile(DurationMs,95) by AppRoleName, bin(TimeGenerated,5m) | where err > 0
// activity log: who changed NSGs
AzureActivity | where OperationNameValue has "networkSecurityGroups" and ActivityStatusValue == "Success" | project TimeGenerated, Caller, OperationNameValue, _ResourceId
// join example with lookup and time windows
let bad = SecurityAlert | where TimeGenerated > ago(1d) | distinct CompromisedEntity;
Heartbeat | where Computer in (bad) | summarize by Computer, ComputerIP
```
Idioms: `ago()`, `bin()`, `summarize ... by bin()`, `arg_max(TimeGenerated,*)` for latest state, `mv-expand` on JSON arrays, `parse_json(Properties)` then `tostring(x.y)`, `has` (indexed term) beats `contains`, `materialize()` for reused subqueries, `render timechart`, `_ResourceId`/`_SubscriptionId`/`_IsBillable`/`_BilledSize` system columns, `ingestion_time()` for lag analysis. Limits: 500 000 rows / 64 MB per query, 10-min timeout; use `take`/`summarize` first.

## Gotchas
- Daily cap hits at a random minute → Sentinel detections and alerts silently stop for the rest of the day; use the cap only as a last resort and alert on `_LogOperation | where Category == "Ingestion" and Operation == "Data collection stopped"`.
- Basic plan tables can't be used in alert rules or joined freely; switching plans allowed once per 30 days per table.
- Retention changes are per table; workspace default only applies to tables without their own.
- Diagnostic settings pointing at the workspace from another region incur egress and are allowed; latency ~2–5 min typical, up to 15 min for some sources — alert windows must respect it.
- Deleting a workspace is soft (14 days) but the name is reserved; `--force` purges.
- `AzureDiagnostics` has a 500-column limit; hitting it drops new columns into `AdditionalFields` — another reason for resource-specific tables.

## Verify
- [ ] `Usage` query shows per-table GB; top 3 tables have a documented reason and plan (Analytics/Basic) decision.
- [ ] Ingestion volume trend flat or explained after transformations; `_BilledSize` for a filtered table drops as expected.
- [ ] Resource-context query works for an app-team member with only Reader on their RG.
- [ ] Shared query pack contains the incident queries; a search job on an archived range returns rows.
