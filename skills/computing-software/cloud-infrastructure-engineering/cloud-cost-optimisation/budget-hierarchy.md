---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.budget-hierarchy
name: budget-hierarchy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, budgeting, budget-hierarchy, budget-scopes, budgets-as-code, organisational-alignment, cost-centres]
level: practitioner
status: docs-checked
description: "Build a budget hierarchy that mirrors the organisation: company, BU, team and project budgets mapped to accounts, tags and cost centres, with roll-up checks and owners."
sources: ["https://www.finops.org/framework/capabilities/budgeting/", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-create.html", "https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets", "https://cloud.google.com/billing/docs/how-to/budgets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Budget hierarchy matching the organisation

Budgets work when each one has an owner who can act on it and the levels add up. Mirror the
management structure, not the cloud resource tree.

## Levels
1. **Company / provider total**: CFO and FinOps lead; set annually.
2. **Business unit**: BU leader and finance partner.
3. **Team / product**: engineering manager; the level where action happens.
4. **Project / initiative** (optional, time-bound): launches, migrations, experiments.

Each level carries: owner, scope definition, amount per month, cost basis (state it: Azure budgets
evaluate actual cost, not amortised), alert thresholds, and parent. The FinOps Budgeting capability
says budgets should be distributed to budget owners across the organisation, tied to the allocation
strategy and cost centres, with holdback and adjustment steps involving higher-level owners and Finance.

## Mapping scopes
| Level | AWS | Azure | Google Cloud |
|---|---|---|---|
| BU | budget on a billing view over the organisation's accounts | management group / MCA billing profile | folder or organisation; reseller subaccount |
| Team | billing view or filters (see Creating a budget) | subscription / resource group, with filters | project(s), service, or one label |
| Project | filters on the budget | filters on the budget | one label (billing-account-level budgets only) |

Azure budgets support management group, subscription, resource group and billing scopes. Google Cloud
budgets can scope to folders and organisations (covering future projects in them), projects, services,
and one label; folder and organisation scope does not cover projects paid by a different billing account.
Native budgets do not do shared-cost splits or virtual tags in the pages read; track the authoritative hierarchy
in your FinOps platform or warehouse and use native budgets only for alerting on directly mapped
scopes.

## Steps
1. Take the org chart and cost-centre list from finance; create the hierarchy table
   (`budget_id, parent_id, owner, scope_rule, month, amount`).
2. Check roll-up: sum of children + unassigned reserve = parent, for each month.
3. Keep a **central/shared** budget for platform and unallocated costs rather than hiding them in
   BU budgets.
4. Create native budgets per directly mapped scope via code (see `budgets-as-code`).
5. Re-map on reorganisations with effective dates; history keeps its old mapping for finance.

## Gotchas
- Budgets on scopes nobody owns (e.g. a shared networking account) get ignored; give them a named owner.
- Overlapping tag filters double count across team budgets.
- A team budget at the payer level with a tag filter misses untagged spend; report it separately.
- Google Cloud labels applied to a project cannot be used as a budget scope, and only one label can be chosen per budget.
- Azure budgets need a single currency across all subscriptions in the scope; multi-currency evaluation is unsupported.

## Verify
- [ ] Children plus reserve add up to each parent for every month.
- [ ] Every budget has a named owner who receives its alerts.

## Checked
Date: 2026-11-08. Confirmed against the FinOps Budgeting capability, the Azure budgets tutorial and the Google Cloud
budgets page (scopes, label limits). The AWS Creating a budget page only confirmed billing-view scoping, so the AWS
cost category and tag filter mappings and the Terraform resource names were removed. Corrected the amortised cost
basis (Azure budgets use actual cost).
Method: documentation only; no commands were run.
