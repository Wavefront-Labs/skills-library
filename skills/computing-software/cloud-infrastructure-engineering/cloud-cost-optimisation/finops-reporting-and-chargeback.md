---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-reporting-and-chargeback
name: finops-reporting-and-chargeback
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-reporting, showback, chargeback, cost-allocation, shared-costs, shared-cost-allocation, amortised-cost, blended-cost, unblended-cost, commitment-amortisation, cost-categories, tagging-compliance, untagged-spend, kubernetes-cost-allocation, kubecost, opencost, focus, cur, unit-economics, cost-per-customer, budgets, forecasting, variance-reporting, finops-foundation, chart-of-accounts, internal-billing]
level: practitioner
status: draft
description: "Report cloud cost per team and product: amortised vs unblended views, allocating shared and Kubernetes costs, showback before chargeback, unit-cost KPIs, and a monthly variance pack."
sources: ["FinOps Foundation - FinOps Framework (allocation, reporting and analytics, invoicing and chargeback)", "FOCUS (FinOps Open Cost and Usage Specification)", "AWS documentation - Cost categories and split charge rules", "OpenCost specification"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FinOps reporting and chargeback — everyone sees their cost, and agrees it's fair

**Goal:** each team and product sees a monthly cost it recognises as its own, including a fair
slice of shared platforms, with trends and unit costs — and, when the organisation is ready,
that cost lands in its budget.

Tagging basics and the waste/rightsize/commit sequence are in
`computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-and-commitments`.

## 1. Pick the cost basis and stick to it
| View | Use |
|---|---|
| **Unblended / billed** | reconciles to the invoice; spiky (upfront purchases land in one month) |
| **Amortised** | spreads upfront and recurring commitment fees over the term and onto the resources that used them — **use for team reporting** |
| **Net amortised** | amortised after negotiated discounts and credits — what the money really is |
Teams on commitments see their rate benefit; the central team carries **unused** commitment cost (or allocate it pro-rata — decide and document). FOCUS columns (`BilledCost`, `EffectiveCost`, `ListCost`) make this consistent across providers.

## 2. Allocation hierarchy
1. **Account/subscription/project per team-environment** — the most reliable key; tags fill in below that.
2. **Tags/labels** (`cost-centre`, `product`, `environment`) for shared accounts; activate them as cost-allocation tags (AWS) — they are not retroactive.
3. **Cost categories / rules** (AWS Cost Categories, Azure cost allocation rules, a mapping table in BigQuery) to map accounts + tags → business units in one place.
4. Report **tag compliance** (% of spend allocatable) — aim > 90-95%; untagged spend is shown as its own line owned by whoever owns that account.

## 3. Shared costs
Shared platforms (networking hub, security tooling, observability, Kubernetes clusters,
support plan, enterprise discount) need a written rule:
- **Proportional** to a driver: cluster cost by requested CPU/memory (not usage, since requests reserve capacity), observability by GB ingested, network by bytes, support plan by share of spend.
- **Even split** only for small, truly fixed costs.
- **Central / not allocated** for genuinely organisational costs, shown as overhead.
Kubernetes: OpenCost/Kubecost or cloud-native split cost allocation (AWS split cost allocation data for EKS/ECS; GKE cost allocation) to get namespace/label costs; idle cluster capacity is reported as a separate line attributed to the platform team or spread by request share.

## 4. Showback, then chargeback
- **Showback** (report only) for at least 2-3 cycles: teams challenge allocations, data gets fixed, trust forms.
- **Chargeback** (cost hits team budgets via finance journals) once allocation is > ~90% and stable. Requires finance agreement on chart-of-accounts mapping, timing (billing closes several days into the month), and a dispute process.
- Commitment purchases: decide whether teams get the discounted rate (incentive aligned) or on-demand rate with the savings retained centrally (funds FinOps). Both are defensible; flipping later causes confusion.

## 5. The monthly pack
Per team: total (amortised) vs budget and forecast; month-over-month and year-over-year
variance with top 5 drivers (by service and resource); unit cost KPI (cost per order, per
active customer, per 1k API calls) — the metric that shows efficiency independently of growth;
open savings recommendations and their status; tag compliance. Executives get the roll-up
plus unit-cost trend; engineers get a self-serve dashboard updated daily.

## Gotchas
- Reporting usage-based cluster costs while capacity is billed by requests leaves a large unallocated idle bucket nobody owns.
- Credits and refunds applied at the invoice level distort team numbers unless allocated explicitly.
- Changing allocation rules mid-year breaks trend lines — restate prior months or annotate.
- Finance month-close vs cloud data lag: final numbers settle days after month-end; label early reports as provisional.
- Chargeback before data quality is good creates disputes instead of savings.

## Verify
- [ ] Reports state the cost basis (amortised/net) and it's consistent month to month.
- [ ] ≥ 90% of spend is allocated to an owner; untagged spend is visible.
- [ ] Each shared cost has a documented allocation driver.
- [ ] Each product reports at least one unit-cost KPI with a trend.
- [ ] Showback ran ≥ 2 cycles with disputes resolved before chargeback started.

Uncertain: compliance and allocation thresholds are common FinOps practice targets, not standards.
