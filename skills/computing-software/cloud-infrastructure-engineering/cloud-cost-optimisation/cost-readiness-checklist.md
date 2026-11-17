---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-readiness-checklist
name: cost-readiness-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-onboarding, cost-readiness-checklist, onboarding-checklist, cost-governance]
level: practitioner
status: draft
description: "Apply a cost-readiness checklist before a workload goes live: ownership, tags, budget, estimate, alerts, unit metric, scheduling, commitments and reviews."
sources: ["https://www.finops.org/framework/capabilities/onboarding-workloads/", "https://www.finops.org/framework/capabilities/planning-estimating/", "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost-readiness checklist for new workloads

Use at account vending and again at the operational readiness review.

## Checklist
- [ ] **Owner** team and accountable manager recorded in the service catalogue.
- [ ] **Accounts/projects** created through vending with business unit and cost centre metadata.
- [ ] **Mandatory tags** applied and passing policy (owner, cost-centre, application, environment).
- [ ] **Cost estimate** for steady state and peak (pricing calculator or Infracost), with assumptions.
- [ ] **Budget** created per environment with alerts at 50/80/100% and forecasted breach alerts.
- [ ] **Anomaly detection** monitors cover the accounts; alerts route to the team channel.
- [ ] **Unit metric** defined (cost per order, per tenant) and the business volume source identified.
- [ ] **Non-production schedules** configured or exempted with reason.
- [ ] **Storage lifecycle and log retention** set.
- [ ] **Data transfer** paths reviewed (cross-AZ, cross-region, NAT, internet egress).
- [ ] **Commitment eligibility**: steady baseline usage flagged to FinOps for coverage after 1-3 months.
- [ ] **Dashboards**: team cost dashboard exists and the team knows where it is.
- [ ] **Review**: first cost review scheduled 30 days after launch to compare actual vs estimate.

## Steps
1. Embed in account vending (metadata required) and ORR templates.
2. Automate checks where possible (tags, budgets, anomaly monitors exist via API).
3. FinOps signs off for workloads above a cost threshold.

## Gotchas
- Checklists applied only at launch miss later changes; re-check at major releases.

## Verify
- [ ] Automated checks run at vending and before go-live.
- [ ] 30-day estimate vs actual review recorded.
