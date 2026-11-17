---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-cost-management
name: sentinel-cost-management
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-cost-management, log-analytics, basic-logs, auxiliary-logs, commitment-tiers, data-lake, retention]
level: advanced
status: docs-checked
description: "Control Microsoft Sentinel cost: choose Analytics, Basic or Auxiliary/data lake plans per table, commitment tiers, retention and ingestion filtering."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/billing", "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs#table-plans", "https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel log tiers and ingestion cost

**Goal:** spend on data that detects or investigates, and store bulk data cheaply.

## 1. Measure
Billing is per meter and each meter is a separate line item in Cost Management (Cost Analysis, Invoice details). Find which tables
and sources drive ingestion before changing anything. Prices change: use the Sentinel pricing page and the cost estimator, never
figures copied into a runbook.

Free data: Azure Activity, Sentinel Health, Office 365 audit logs (SharePoint, Exchange admin, Teams) and security alerts from the
Defender products do not cost ingestion. The raw logs of some Defender XDR, Defender for Endpoint/Identity/Office 365/Cloud Apps,
Entra ID and AIP data types are paid even though the alerts are free.

## 2. Choose the plan per table
| Plan | Documented position |
|---|---|
| Analytics | Best for high-value data used for continuous monitoring and real-time detection; query price included; analytics retention is 30 days, 90 for Sentinel (extendable to two years) |
| Basic | Medium-touch data for troubleshooting and incident response; reduced ingestion cost; query price not included; alerts limited to Simple Log Alerts; Log Analytics query scope only |
| Auxiliary / Lake | Low-touch data such as verbose logs and audit/compliance data; minimal ingestion cost; slower queries, not optimised for real-time analysis; no alerts |

- Basic and Auxiliary are not available for workspaces in legacy (classic) pricing tiers. Only some Azure tables and DCR-based
  custom tables support Basic or Auxiliary.
- Sentinel data lake tier meters: ingestion, processing, storage (billed on a 6:1 compression assumption), query (per GB scanned
  by KQL or KQL jobs) and advanced data insights (notebooks, per compute hour). Ingestion and processing charges do not apply to
  tables whose retention includes both analytics and data lake tiers.
- Change a table's plan or retention in the portal under Data management > Tables.

## 3. Commitment tiers (Analytics)
Pay-as-you-go is the default. Commitment tier pricing starts at 100 GB per day, usage above the tier is billed at that tier's
effective rate, and billing is daily. You can increase a tier at any time (this restarts the 31-day commitment); you can lower it,
or return to pay-as-you-go, only after the 31-day commitment period. Changing the tier needs Contributor or Owner on the workspace.
Check the current tier under Settings > Pricing.

Other levers on the same page: a pre-purchase plan of Sentinel commit units (one year term), and a Log Analytics dedicated cluster
if you ingest at least 100 GB per day across workspaces in one region (limits: two clusters per region and subscription, up to
1000 linked workspaces, same region only).

## 4. Reduce at source
- Keep non-security operations data in a separate workspace so it does not incur Sentinel analysis cost.
- Put secondary, lower-fidelity security data in the data lake / Lake tier instead of Analytics.
- For Windows Security Events through the Azure Monitor Agent, use data collection rules: choose All, Common or Minimal, or build
  custom filters so unselected events are left behind at the source.
- CEF extras land in the AdditionalExtensions field, whose volume is variable and can exceed the standard CEF fields.

## 5. Retention
Analytics retention is free for the first 90 days with Sentinel; beyond that, standard Log Analytics retention prices apply.
Total retention (analytics plus long-term / data lake) can reach 12 years and is much cheaper; older data is read through data
lake exploration or KQL.

## Gotchas
- Moving a table to Basic or Auxiliary changes which features work (alerts, Insights, restore, export): review the rules and
  workbooks that use the table first.
- Removing Sentinel does not remove the Log Analytics workspace or its charges.
- After 31 March 2027 Sentinel is supported only in the Defender portal; menu paths above are the Azure portal ones.

## Checked
Date: 2026-11-08.
Confirmed against the three cited Learn pages: free data sources, plan comparison, retention limits, commitment tier rules
(100 GB per day start, 31-day lowering rule, Contributor/Owner), dedicated cluster limits, data lake meters, DCR filtering.
Removed because the pages do not state them: the Usage and CommonSecurityLog KQL queries, the `az monitor log-analytics workspace
table update --plan Basic` command, the "limited KQL" and "per-query charge" wording for Basic (the page lists full KQL and no
included query price), the daily-cap and Defender XDR streaming advice, and the "2 years interactive" wording.
Method: docs-only read of cited pages, 2026-11-08
