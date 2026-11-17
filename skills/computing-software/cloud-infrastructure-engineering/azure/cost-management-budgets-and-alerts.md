---
id: computing-software.cloud-infrastructure-engineering.azure.cost-management-budgets-and-alerts
name: cost-management-budgets-and-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cost-management, budgets, cost-analysis, cost-alerts, finops, anomaly-alerts, cost-exports, focus, showback, chargeback, cost-allocation, tagging, amortized-cost, actual-cost, pricing-calculator, ea, mca, csp, usage-details, action-groups, cost-management-reader]
level: practitioner
status: draft
description: "Set up Azure Cost Management: budgets with action groups, anomaly alerts, scheduled exports (FOCUS) to storage, amortized vs actual views, cost allocation rules and tag inheritance for showback."
sources: ["Microsoft Learn - Tutorial: Create and manage budgets", "Microsoft Learn - Identify anomalies and unexpected changes in cost", "Microsoft Learn - Tutorial: Create and manage exported data (FOCUS)", "Microsoft Learn - Group and allocate costs using tag inheritance", "FinOps Foundation - FOCUS specification"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost Management — budgets that page someone, exports you can query

**Goal:** no month-end surprise. Every subscription has a budget and anomaly alert
wired to a human; raw cost data lands in a lake daily; teams can see their own spend.

## 1. Views and scopes
- Cost analysis scopes: billing account (EA/MCA) → department/invoice section →
  subscription → resource group. RBAC: *Cost Management Reader* at the management group
  for central FinOps; *Billing Reader* for invoices.
- **Actual** cost shows reservation/savings-plan purchases as spikes on purchase day;
  **Amortized** spreads them over the term and attributes them to the resources that
  used them — use amortized for showback, actual for reconciling invoices.
- Costs lag 8–24 h; usage for the last day is always partial. Marketplace and
  reservations appear under separate charge types (`Purchase`, `Usage`, `Refund`).

## 2. Budgets
```bash
az consumption budget create-with-rg -g rg-app-prod --budget-name rg-app-prod-monthly \
  --amount 5000 --time-grain Monthly --start-date 2026-10-01 --end-date 2028-09-30 \
  --category Cost
```
Portal/ARM `Microsoft.Consumption/budgets` is richer: notifications at **actual** 80/100 %
and **forecasted** 100 % (forecast needs ~2 weeks of history), each pointing at an
**action group** (email + Teams webhook + optional Function/Logic App that scales down or
locks the RG). Budgets never stop spend by themselves; the automation does.
Filters: by tag (`cost-centre`), resource group, or meter category.
One budget per subscription minimum, plus per cost-centre tag at the billing scope.

## 3. Anomaly detection
Subscription scope → *Cost alerts > Anomaly alert* (one per subscription, email
recipients). The model flags daily-cost departures from the 60-day pattern; look at the
anomaly in Cost analysis with **Daily** granularity grouped by `ResourceId` to find the
new storage egress or the forgotten GPU VM.

## 4. Exports (the FinOps data lake)
`Cost Management > Exports > Create` — type **Cost and usage details (FOCUS)** (vendor-
neutral columns: `BilledCost`, `EffectiveCost`, `ServiceCategory`, `Tags`), daily
*month-to-date* overwrite or daily incremental, parquet, to a storage account with
file partitioning on. Point Synapse serverless/Databricks/Power BI at it. The FinOps
toolkit's *FinOps hubs* deploys this plus Data Explorer dashboards in one Bicep.
Alternative: *Cost Management connector for Power BI* (EA/MCA only, pulls amortized data).

## 5. Allocation and showback
- Tag inheritance (`Cost Management > Manage subscription > Tag inheritance`) copies
  subscription/RG tags onto usage records so untagged resources still allocate — no
  resource changes needed.
- **Cost allocation rules** (EA/MCA) redistribute shared costs (hub networking, Log
  Analytics, Defender) to teams by % or proportional to their own compute cost.
- Azure Policy `Modify` effect to add `cost-centre` from RG; `Deny` creation without it
  on new RGs. Report untagged with Resource Graph:
  `resources | where isnull(tags['cost-centre']) | summarize count() by subscriptionId`.

## 6. Quick wins that budgets reveal
Deallocate (not just stop) dev VMs; unattached managed disks and public IPs; Log
Analytics ingestion (see log-analytics skill); Premium storage on cold data; idle
Application Gateways/Firewalls in sandboxes (~£/hour whether used or not); orphaned
snapshots. Advisor *Cost* recommendations give the list with projected savings.

## Gotchas
- Budget notifications require the action group/contact to exist *and* the budget creator
  to keep Cost Management permissions; alerts stop silently otherwise.
- Budgets at RG scope evaluate every ~4–12 h, not real time; a runaway can overshoot by a day.
- CSP subscriptions: partner-earned credit and retail rates differ from pay-as-you-go; exports show the partner price, not list.
- `az consumption` is deprecated-ish — prefer `az costmanagement` and ARM for new automation.
- Reservation purchases in **actual** view can trip a budget's 100 % threshold on day one; filter budgets to `Usage` charge type if that annoys finance.

## Verify
- [ ] Every production subscription: ≥1 budget with forecast alert + anomaly alert listed under *Cost alerts*.
- [ ] Test: lower a sandbox budget below MTD spend; alert email/Teams arrives within the evaluation window.
- [ ] FOCUS export writes a parquet file today under the expected path; `EffectiveCost` sums to Cost analysis amortized total ±1 %.
- [ ] Untagged-resource query returns zero in production RGs.
