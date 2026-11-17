---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-funding-model
name: cloud-funding-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-funding-model, capex-to-opex, migration-funding, double-running, provider-incentives, financial-model]
level: practitioner
status: draft
description: "Build the cloud financial and funding model: migration programme budget, double-running costs, provider credits and incentives, opex shift and who pays for shared platforms."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/financial-considerations/", "https://aws.amazon.com/migration-acceleration-program/", "https://www.finops.org/framework/capabilities/budgeting/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud funding and financial model

## Cost categories to fund
1. **Migration programme**: people (internal + partner), tooling, training.
2. **Double running**: on-prem and cloud in parallel during waves (often 6-18 months).
3. **Landing zone and platform**: shared networking, security tooling, logging, platform team.
4. **Run costs** of migrated workloads (opex) and commitments.
5. **Exit costs**: DC contract penalties, hardware disposal, licence true-ups.

## Offsets
- Provider migration incentives (AWS MAP credits, Azure Migrate and Modernize / Innovate offers,
  Google migration programs) tied to committed workloads; read the eligibility.
- Avoided hardware refresh capex, DC lease, power, support contracts.
- Licence savings from consolidation or BYOL/Azure Hybrid Benefit.

## Funding models for shared platform
Central funding (simple, encourages adoption) vs showback/chargeback with a platform fee
(accountability). Many start central and introduce allocation once adoption is high.

## Steps
1. Model month by month: on-prem cost curve declining as waves complete, cloud curve rising.
2. Identify the peak double-running month and fund it explicitly.
3. Agree capex/opex treatment with finance (capitalising migration labour where policy allows).
4. Track actuals vs model monthly.

## Gotchas
- Business case that assumes on-prem costs disappear on migration day.
- Credits treated as permanent savings.

## Verify
- [ ] Month-by-month model approved by finance.
- [ ] Double-running peak funded.
