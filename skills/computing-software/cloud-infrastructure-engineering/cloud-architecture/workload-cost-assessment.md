---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.workload-cost-assessment
name: workload-cost-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, workload-cost-assessment, tco, migration-business-case, cost-modelling]
level: practitioner
status: draft
description: "Assess current and target cost per application for migration: allocate on-prem cost, model cloud run cost per strategy, add migration and dual-running costs."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-planning/welcome.html", "https://learn.microsoft.com/azure/migrate/concepts-business-case-calculation", "https://cloud.google.com/migration-center/docs/migration-center-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workload cost assessment per application

## Steps
1. **Current cost per app**: allocate data centre (space, power, cooling), hardware
   depreciation, licences, support contracts, storage, network and staff time to each
   application using drivers (VMs, cores, TB, tickets). Shared costs need an explicit key.
2. **Target cost per app per strategy**: rehost (rightsized compute from utilisation data,
   storage, backup, egress), replatform (managed DB, containers), refactor. Use the provider
   calculators or migration tools' assessment reports (Azure Migrate business case, AWS
   Migration Evaluator, Google Migration Center).
3. **Include licensing effects**: BYOL vs licence-included, Windows/SQL benefits, Oracle
   core factors on cloud vCPUs.
4. **One-off costs**: migration labour, tools, training, dual running during cutover,
   contract exit penalties.
5. **Avoided costs that are real**: hardware refresh not bought, DC exit; flag avoided costs
   that are not realisable (sunk depreciation, staff not redeployed).
6. **Rank apps** by savings and effort to feed wave prioritisation.

## Gotchas
- Comparing allocated on-prem hardware to unrightsized cloud overstates cloud cost.
- Leaving out egress and support plans understates it.

## Verify
- [ ] Per-app current vs target cost with stated allocation keys.
- [ ] One-off and dual-running costs included.
