---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.post-onboarding-review
name: post-onboarding-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, onboarding-workloads, workload-onboarding, post-onboarding-review, post-migration-optimisation, estimate-accuracy]
level: practitioner
status: draft
description: "Run the first 90-day cost review of a newly onboarded workload: actuals vs estimate, rightsizing, commitments, tagging, unit cost and closing the business case."
sources: ["https://www.finops.org/framework/capabilities/onboarding-workloads/", "https://www.finops.org/framework/capabilities/workload-optimization/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First 90-day cost review

New workloads are usually over-provisioned "to be safe" and missed in commitments. A scheduled
review after go-live catches this while the team still remembers the design.

## Checkpoints
- **Day 30**: tags and allocation correct, budget and anomaly alerts firing to the right channel,
  actuals vs estimate ramp, obvious waste (idle non-prod, oversized test instances).
- **Day 60**: rightsizing from real utilisation (Compute Optimizer, Azure Advisor, GCP
  Recommender, Kubernetes VPA recommendations), storage tiers and lifecycle rules, log retention.
- **Day 90**: steady-state confirmed; add to commitment planning; unit cost measured vs target;
  business case updated (for migrations: on-prem decommission status and realised savings).

## Review agenda (45 minutes, technical owner + FinOps + finance partner)
1. Actuals vs estimate by service, explain variances > 20%.
2. Top 10 resources by cost: right size, right tier, right purchasing option.
3. Data transfer and logging (frequently underestimated).
4. Non-prod schedules and environment sprawl.
5. Actions with owners and savings; next forecast update.

## Steps
1. Create the review tasks automatically at intake (calendar plus tickets).
2. Pull a standard review pack from the cost warehouse by account/tag.
3. Record estimate accuracy per service to improve future estimates.
4. Close the workload's onboarding record when the day-90 actions are done.

## Gotchas
- Reviewing too early (week 1) when usage has not ramped.
- Rightsizing during a launch peak; use at least 2-4 weeks of representative data.

## Verify
- [ ] Day 30/60/90 reviews held with logged actions.
- [ ] Estimate accuracy recorded and the workload is in commitment planning.
