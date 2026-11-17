---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.workload-intake
name: workload-intake
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, onboarding-workloads, workload-onboarding, workload-intake, cost-estimation, migration-planning]
level: practitioner
status: draft
description: "Run a workload intake process for FinOps: intake form, cost estimate and owner, account and tagging setup, budget, commitment impact and approval gates."
sources: ["https://www.finops.org/framework/capabilities/onboarding-workloads/", "https://www.finops.org/framework/capabilities/planning-estimating/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workload intake process

Every new workload (greenfield or migrated) should enter the cloud with an owner, an estimate and
the controls already in place. Intake is the cheapest point to get this right.

## Intake form (minimum fields)
- Workload name, business owner, technical owner, cost centre, business unit.
- Purpose and business value (revenue, customers, compliance).
- Expected go-live date, environments (prod, non-prod), regions.
- Architecture summary and cost estimate (pricing calculator / Infracost output) for month 1,
  month 6 and month 12; unit metric expected (cost per customer etc.).
- Data classification and residency (drives region and service choices).
- Commitment impact: steady-state compute/database that could be committed after stabilising.

## Steps
1. **Submit** via a ticket or portal form; FinOps and the cloud platform team review together.
2. **Review estimate** against similar workloads; challenge missing data transfer, logging and
   non-prod costs (commonly forgotten).
3. **Provision** accounts/subscriptions/projects via the landing zone vending process with
   mandatory tags, budget and anomaly alerts pre-wired.
4. **Approve** by threshold: small workloads auto-approve; large ones (e.g. > $20k/month) need
   finance sign-off and inclusion in the budget/forecast.
5. **Add to forecast** with the ramp curve; tell the commitment planner about expected steady
   state.
6. **Schedule** the post-onboarding review (30/60/90 days).

## Gotchas
- Intake that takes weeks drives teams to shadow accounts; keep the small path fast.
- Estimates without a ramp curve make month 1 look like a huge overrun or underrun.

## Verify
- [ ] Every new account has an intake record with owner, estimate and budget.
- [ ] New workloads appear in the forecast before go-live.
