---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.allocation-coverage
name: allocation-coverage
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, allocation, allocation-coverage, allocatable-spend, tagging-compliance, finops-kpis, unallocated-costs]
level: practitioner
status: docs-checked
description: "Measure and raise allocation coverage: define the KPI and denominator, compute it from billing data, track by team and provider, and use the FinOps Crawl/Walk/Run guidance."
sources: ["https://www.finops.org/framework/capabilities/allocation/", "https://www.finops.org/wg/finops-kpis/", "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html", "https://focus.finops.org/docs/specification/v1-4/columns/cost-and-usage/effective-cost/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocation coverage KPI

"What percent of spend can we put an owner on?" is the first number executives ask for and the
first KPI of an allocation programme.

## Definition
```text
allocation coverage = allocated cost / total allocatable cost
```
- **Allocated** = cost with a valid owner from any mechanism: account/subscription/project mapping,
  tags/labels, virtual tagging rules, shared-cost split rules. The FinOps Allocation capability lists
  accounts, projects, subscriptions, resource groups, tags/labels and derived metadata (such as a CMDB) as sources.
- **Total allocatable** = all EffectiveCost minus categories you deliberately exclude (tax,
  enterprise support, credits) - state the exclusions in the KPI definition.
- "Valid" means the value exists in the owner registry, not just non-empty (`team=test` fails).
- Related FinOps framework KPI wording: "Percentage of technology costs allocated directly to organizational
  units", its inverse "Percentage of costs that cannot be categorized and allocated directly", and
  "Percentage of costs with appropriate allocation metadata".

## Compute
```sql
SELECT BillingPeriodStart,
  SUM(CASE WHEN owner IS NOT NULL AND owner IN (SELECT team FROM registry) THEN EffectiveCost END)
  / SUM(EffectiveCost) AS allocation_coverage
FROM focus_costs_enriched
WHERE ChargeCategory IN ('Usage','Purchase')
GROUP BY 1 ORDER BY 1;
```
`EffectiveCost` and `ChargeCategory` (values Usage, Purchase, Tax, Credit, Adjustment) are FOCUS 1.4 columns;
`owner` and `registry` are your own enrichment table and owner list.
Also report **tag coverage** (by tags alone) separately: it shows how much depends on rules that
may break.

## Maturity guidance (FinOps Allocation capability; no percentage thresholds are published, set your own)
- Crawl: costs of accounts, projects or subscriptions are allocated to cost centres from a known list;
  tagging compliance is inconsistent; shared costs go to central budgets.
- Walk: a majority of cost is allocated directly, tagging is followed in key areas, shared costs are split
  by a proportional, fixed or even-split model, and allocation KPIs are understood but not automated.
- Run: allocation at any required granularity, ownership and metadata enforced as a precondition for
  provisioning, KPIs automated, and shared costs distinguished from dedicated costs.

## Steps
1. Publish the definition and exclusions.
2. Break down unallocated cost by provider, account, service and resource type; top 20 items
   usually explain most of the gap.
3. Fix at source: account-per-team, tag policies on creation, untaggable services handled by rules
   (see `unallocated-costs`, `virtual-tagging`).
4. Track weekly per BU; include in the monthly pack with trend.

## Gotchas
- Compute coverage over EffectiveCost: FOCUS defines it as billed cost with upfront purchases recognised
  against the usage they cover, so one upfront purchase does not swing the KPI.
- Allocating everything to a "shared" bucket raises the number without adding ownership; report
  shared separately. The FinOps page also says to distinguish shared from dedicated costs.
- AWS cost allocation tags must be activated in the Billing and Cost Management console, can take up to 24 hours
  to appear, and only the management account (or a standalone account) can manage them. AWS documents a
  "Backfill cost allocation tags" topic, so check it before assuming history cannot be improved.

## Verify
- [ ] KPI definition with exclusions is published.
- [ ] The monthly coverage trend is visible per BU and provider.

## Checked
Date: 2026-11-08. Confirmed against the FinOps Allocation capability page, the FinOps KPIs page (library page
only, individual KPI formulas not shown), the AWS cost allocation tags page and the FOCUS 1.4 ChargeCategory and
EffectiveCost column pages. Removed the invented 60/80/90 percent targets and the claim that tag history never
improves. The AWS backfill topic itself was not read.
Method: documentation only; no commands were run.
