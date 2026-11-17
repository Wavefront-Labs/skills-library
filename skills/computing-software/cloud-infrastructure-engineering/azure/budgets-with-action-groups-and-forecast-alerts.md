---
id: computing-software.cloud-infrastructure-engineering.azure.budgets-with-action-groups-and-forecast-alerts
name: budgets-with-action-groups-and-forecast-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cost-management, budgets, budget-alerts, forecast-alerts, budget-action-group, consumption-budget, automation]
level: practitioner
status: docs-checked
description: "Create Azure budgets at subscription/RG/MG scope with actual and forecast thresholds, filters, action groups that notify or trigger automation, and deploy them as code."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets", "https://learn.microsoft.com/azure/cost-management-billing/manage/cost-management-budget-scenario", "https://learn.microsoft.com/azure/templates/microsoft.consumption/budgets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Budgets with action groups and forecast alerts

**Goal:** every subscription has a budget that warns on forecast before money is spent, notifies
the owning team, and (in sandboxes) can act automatically.

## Design
An example threshold plan (a design choice, not a Microsoft default):
| Threshold | Type | Action |
|---|---|---|
| 80% | Forecasted | Email team DL |
| 100% | Forecasted | Email + webhook |
| 100% | Actual | Email + action group (ticket) |
Budgets **don't stop spending** by themselves: notifications fire when thresholds are exceeded, resources are
not affected and consumption is not stopped. Budgets are evaluated against cost data every 24 hours,
so don't expect real-time alerts. Forecasted alerts warn that spending trends are likely to exceed the budget.

## Bicep (subscription scope)
```bicep
targetScope = 'subscription'
resource budget 'Microsoft.Consumption/budgets@2023-11-01' = {
  name: 'budget-monthly'
  properties: {
    category: 'Cost'
    amount: 5000
    timeGrain: 'Monthly'
    timePeriod: { startDate: '2026-10-01' }   // first day of a month
    filter: { tags: { name: 'Environment', operator: 'In', values: [ 'prd' ] } }
    notifications: {
      forecast80: { enabled: true, operator: 'GreaterThan', threshold: 80, thresholdType: 'Forecasted', contactEmails: [ 'team-orders@contoso.com' ] }
      actual100:  { enabled: true, operator: 'GreaterThan', threshold: 100, thresholdType: 'Actual', contactGroups: [ actionGroup.id ], contactRoles: [ 'Owner' ] }
    }
  }
}
```
Deploy via subscription vending so new subs are born with a budget.

## Action group automation
Action groups can trigger automation such as Azure Functions, Webhooks or Runbooks. Microsoft's
budget scenario (runbook to stop VMs by webhook) reads fields of the budget alert payload such as
`SubscriptionId`, `BudgetName` and `NotificationThresholdAmount`.
Action groups are currently supported only for subscription and resource group budget scopes.
Make sure the StartDate of a monthly budget is the first day of the current month.

## Scopes
Budgets can be created at billing account and management group scopes as well as subscription and resource group.
A budget at management group or billing account scope operates under a single currency; multi-currency
evaluations are not supported and alerts may be missed.

## Gotchas
- Pick the action group for notifications deliberately; common alert schema is applied for budget alerts either way.
- When a budget expires it is automatically deleted.

## Verify
- [ ] Each subscription lists a budget with the expected amount and thresholds.
- [ ] A test with a tiny budget amount on a sandbox triggers the action group at the next evaluation (up to 24 h).

## Checked

Method: docs-checked 2026-11-09 against the three cited pages, downloaded and searched. Read the tutorial passages on forecasted alerts, 24-hour evaluation, action group scopes, StartDate, currency and expiry, the budget scenario payload field names and webhook runbook, and the ARM template reference property names (api 2023-11-01, contactGroups, contactRoles, thresholdType, startDate, tags filter). Dropped: runbook with Stop-AzVM and role, 120% sandbox row, cost data lag range, amortized-cost note, az consumption command, startDate-in-the-past rule, 10-year default end date.
