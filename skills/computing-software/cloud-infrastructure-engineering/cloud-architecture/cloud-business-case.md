---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-business-case
name: cloud-business-case
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, togaf, cloud-business-case, npv, tco, benefits-realisation]
level: advanced
status: draft
description: "Build a cloud business case: baseline cost, target run cost, migration and double-running costs, benefits beyond cost, NPV/payback and sensitivity."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/cloud-migration-business-case", "https://docs.aws.amazon.com/whitepapers/latest/how-aws-pricing-works/aws-pricing-overview.html", "https://www.finops.org/framework/capabilities/planning-estimating/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud business case

## Steps
1. **Baseline (do nothing)** over 3-5 years: hardware refresh, datacentre lease and power,
   licences and support, staff time, network, DR site. Include planned refreshes; leaving
   them out favours on-prem unfairly.
2. **Target run cost**: priced from rightsized utilisation data, not current allocations;
   include support plan, backup, monitoring, egress, security tooling, and expected
   commitment discounts after year one.
3. **One-off migration costs**: assessment, partner fees, tooling, re-platforming effort,
   training, data transfer, testing.
4. **Double running**: both estates in parallel during waves (often 6-18 months). Commonly
   the most underestimated line.
5. **Benefits beyond cost** with metrics: faster releases, avoided outages, new-region
   launch time, staff redeployed. Quantify only where finance accepts the method;
   list the rest qualitatively.
6. **Financials**: cash flow per year, NPV at the company discount rate, payback period,
   capex vs opex profile (finance cares about EBITDA impact).
7. **Sensitivity**: vary utilisation, discount level, migration duration and stranded
   on-prem assets; show the break-even.
8. **Benefits-realisation plan**: owner, measure and date per benefit; review after go-live.

## Gotchas
- Lift-and-shift of over-provisioned VMs makes cloud look expensive; rightsizing is part of the case.
- Sunk-cost assets with years of depreciation left reduce near-term savings.

## Verify
- [ ] Finance has reviewed baseline and discount rate.
- [ ] Sensitivity table shows the assumptions that flip the decision.
