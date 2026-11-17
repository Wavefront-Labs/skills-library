---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-business-outcomes
name: cloud-business-outcomes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, togaf, cloud-business-outcomes, business-drivers, okrs, cloud-adoption-framework]
level: practitioner
status: draft
description: "Turn business drivers into measurable cloud business outcomes: agility, cost, resilience and innovation metrics with baselines, targets and owners."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/business-outcomes/", "https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/business-outcomes.html", "https://pubs.opengroup.org/togaf-standard/adm/chap03.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business drivers and cloud business outcomes

"Move to cloud" is not an outcome. Each driver needs a metric, a baseline, a target and a
business owner who cares about it.

## Steps
1. **Collect drivers** from strategy and interviews: datacentre contract exit, growth, M&A,
   new markets, regulatory change, talent, security posture, cost pressure.
2. **Translate into outcome categories** (CAF uses fiscal, agility, global reach, customer
   engagement, performance):
   - fiscal: run-cost per unit, capex avoided, datacentre exit date;
   - agility: lead time for changes, environment provisioning time, deployment frequency;
   - resilience: availability, RTO/RPO achieved in tests;
   - reach: time to launch in a new region;
   - security: mean time to remediate critical findings.
3. **Baseline now** (you cannot claim improvement without it) and set dated targets.
4. **Assign an owner** outside IT where possible; outcomes owned only by IT lose funding.
5. **Link workloads to outcomes** so prioritisation of migration waves follows value.
6. **Report quarterly** against targets; adjust the plan when outcomes are not moving.

## Gotchas
- Cost savings as the only outcome usually disappoints in year one (double running, re-skilling).
- Vanity metrics (number of workloads migrated) measure activity, not value.

## Verify
- [ ] Each outcome has metric, baseline, target date and named owner.
- [ ] Migration backlog is ordered with reference to outcomes.
