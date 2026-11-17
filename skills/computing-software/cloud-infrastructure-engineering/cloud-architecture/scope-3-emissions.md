---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.scope-3-emissions
name: scope-3-emissions
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, sustainability, scope-3-emissions, ghg-protocol, carbon-accounting, customer-carbon-footprint, emissions-reporting, csrd]
level: practitioner
status: draft
description: "Report cloud usage as Scope 3 emissions: GHG Protocol categories, provider carbon tools and their methods, market vs location based figures, gaps and audit evidence."
sources: ["https://ghgprotocol.org/standards/scope-3-standard", "https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/", "https://learn.microsoft.com/industry/sustainability/api-calculation-method", "https://cloud.google.com/carbon-footprint/docs/methodology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scope 3 cloud emissions reporting

## Steps
1. **Classify correctly.** For a cloud customer, purchased cloud services fall in GHG Protocol
   Scope 3 Category 1 (purchased goods and services). The provider's Scope 1 and 2 become
   your Scope 3. On-premises data centres stay in your Scope 1 and 2.
2. **Collect provider data**:
   - AWS Customer Carbon Footprint Tool (Billing console; data exports available), monthly.
   - Microsoft Emissions Impact Dashboard / Azure carbon optimization, covering Scopes 1-3
     of Azure usage.
   - Google Cloud Carbon Footprint with BigQuery export, location- and market-based.
3. **Understand each method**: location-based vs market-based Scope 2 inside the provider
   figure, whether embodied (manufacturing) emissions are included, allocation basis
   (spend, usage), data latency (often 1-3 months) and rounding. Document differences when
   aggregating across clouds.
4. **Fill gaps** for SaaS and smaller providers using spend-based emission factors (EEIO
   factors) and flag them as estimates.
5. **Allocate internally** by account/project/tag to business units so teams own their figures.
6. **Prepare for assurance**: keep exports, method notes and change logs; frameworks such as
   CSRD (ESRS E1) and ISSB IFRS S2 require disclosed methods and limited assurance.
7. Supplement with engineering metrics (SCI, utilisation) since provider reports are too
   coarse and delayed to steer daily decisions.

## Gotchas
- Provider tools change methodology; restate prior periods or note the break.
- Market-based figures near zero do not mean zero impact; report both where available.
- Mixing spend-based estimates and measured data without labels misleads auditors.

## Verify
- [ ] Monthly cloud Scope 3 figures stored per provider with method notes.
- [ ] Allocation by business unit reconciles to the provider total.
