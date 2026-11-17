---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.day-one-cost-controls
name: day-one-cost-controls
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-onboarding, day-one-cost-controls, account-vending-finops, default-budgets, mandatory-tags, cost-guardrails]
level: practitioner
status: draft
description: "Bake cost controls into every new account or subscription at creation: budgets and alerts, mandatory tags, owner contacts, anomaly monitors, SKU guardrails and showback."
sources: ["https://www.finops.org/framework/capabilities/onboarding-workloads/", "https://docs.aws.amazon.com/controltower/latest/userguide/account-factory-for-terraform.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Day-one cost controls for new accounts

## Baseline applied by the vending pipeline
1. **Ownership metadata**: owner team, cost centre, environment, application, budget owner email
   as account tags (AWS account tags / Azure subscription tags / GCP project labels).
2. **Budget** at the account scope with forecasted and actual alerts to the owner and FinOps.
3. **Anomaly monitor** scoped to the account/team.
4. **Tag policies** and enforcement (tag inheritance from the account/subscription where supported).
5. **Guardrails** by environment: allowed regions/SKUs, no commitment purchases, sandbox lease expiry.
6. **Cost visibility**: account mapped to team in allocation rules; team dashboard link sent at creation.
7. **Non-prod schedules**: default off-hours tags for dev/test.

## Steps
1. Add the controls to the vending module (AFT customisations, Azure subscription vending module,
   GCP project factory).
2. Require inputs (cost centre, budget amount) at request time; reject without them.
3. Backfill existing accounts with a one-off campaign.

## Gotchas
- Budgets created with placeholder amounts nobody updates; require realistic estimate.
- Owner emails pointing at individuals who leave; use team distribution lists.

## Verify
- [ ] New account has budget, monitor, tags and allocation mapping within an hour of creation.
