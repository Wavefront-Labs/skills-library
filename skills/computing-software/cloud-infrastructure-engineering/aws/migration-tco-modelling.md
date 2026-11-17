---
id: computing-software.cloud-infrastructure-engineering.aws.migration-tco-modelling
name: migration-tco-modelling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, tco, migration-evaluator, business-case, pricing-calculator, rightsizing]
level: practitioner
status: draft
description: "Build a credible on-premises vs AWS TCO for a migration business case: data collection, right-sizing, licensing, commitments, dual-running costs and the common distortions."
sources: ["AWS Migration Evaluator User Guide - Overview and Quick Insights", "AWS Prescriptive Guidance - Building a business case for migration", "AWS Pricing Calculator User Guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration TCO modelling

## Collect real utilisation
- **Migration Evaluator** agentless collector (or imports from RVTools, CMDB, monitoring exports)
  gathers CPU, memory, storage and uptime for 2-4 weeks; produces a Quick Insights business case.
- Without utilisation data, models size AWS to allocated capacity and overstate cost by 30-60%.

## On-premises side (fully loaded)
| Cost | Include |
|---|---|
| Hardware | servers, storage, network, refresh cycle amortised (3-5 years), maintenance contracts |
| Facilities | rack space, power and cooling (kW x PUE x tariff), colocation fees |
| Software | hypervisor, OS, database licences and support, backup and monitoring tools |
| People | admin FTE time for hardware, virtualisation, storage, DC operations |
| Risk | DR site, over-provisioning for peak |

## AWS side
- Right-size from P95 utilisation, choose current-generation (Graviton where software allows).
- Apply commitments: Savings Plans/RIs for steady baseline, On-Demand/Spot for the rest.
- Storage tiers (gp3, S3 classes with lifecycle), backup storage, data transfer out, support plan (% of spend), monitoring and security services.
- Licensing: licence-included vs BYOL (Dedicated Hosts for some Microsoft/Oracle terms), and the chance to move SQL Server/Oracle to open-source engines.
- Model in **AWS Pricing Calculator** per application, exported and versioned.

## Migration costs and timeline
- Dual running (both estates during waves), migration tooling and partner services, training,
  data transfer for seeding, contract termination penalties.
- Funding offsets: MAP (Migration Acceleration Program) credits, partner funding; get them in writing.
- Model by year (3-5 years) with the wave plan: costs fall as on-prem is decommissioned, not on day one.

## Common distortions
- On-demand list prices vs depreciated, sunk hardware.
- Ignoring staff productivity and agility; or the opposite, counting headcount savings that will not happen.
- Forgetting egress and inter-AZ traffic for chatty applications.
- Comparing peak-sized on-prem to peak-sized AWS instead of using elasticity.

## Verify
- [ ] Model reviewed by finance with stated assumptions and sensitivity (+/- 20% utilisation, commitment coverage).
- [ ] Post-migration actuals compared against the model at 6 and 12 months.
