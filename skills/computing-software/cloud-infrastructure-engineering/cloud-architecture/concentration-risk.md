---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.concentration-risk
name: concentration-risk
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, ecosystem-roles, concentration-risk, dora, critical-ict-third-party, outsourcing-register, exit-plan, substitutability, eba-outsourcing]
level: advanced
status: draft
description: "Assess and manage cloud concentration risk for regulated firms: DORA register of information, substitutability, exit plans, multi-region versus multi-provider mitigation."
sources: ["https://eur-lex.europa.eu/eli/reg/2022/2554/oj", "https://www.eba.europa.eu/regulation-and-policy/internal-governance/guidelines-on-outsourcing-arrangements", "https://www.bankofengland.co.uk/prudential-regulation/publication/2021/march/outsourcing-and-third-party-risk-management-ss"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud concentration risk

## What regulators expect
- **EU DORA** (applies from 17 Jan 2025): ICT third-party risk strategy, a **register of
  information** on all ICT contracts, assessment of concentration risk before contracting, exit
  strategies for services supporting critical or important functions, and oversight of critical
  ICT third-party providers (CTPPs) designated by the ESAs.
- **EBA outsourcing guidelines** and UK PRA SS2/21: materiality assessment, exit plans that are
  documented and tested, substitutability analysis.

## Assessment steps
1. Map critical/important business functions to the cloud services and regions they depend on
   (from BIA and dependency mapping).
2. For each provider: share of critical functions, substitutability (time and cost to move),
   intra-group concentration (same provider via SaaS vendors - fourth parties).
3. Rate: impact of provider-wide outage, regional outage, contract termination, provider failure.
4. Choose mitigations proportionate to impact:
   - Multi-AZ / multi-region within one provider (covers most outage scenarios).
   - Stressed exit plan: documented runbook to move to another provider or on-prem within a
     stated timeline, with data export tested.
   - Multi-provider active capacity only for functions where a provider-wide outage is
     intolerable; it is expensive and reduces the use of managed services.
5. Record in the register; report to management body annually.

## Gotchas
- Fourth-party concentration: several SaaS vendors on the same provider and region.
- Exit plans that were never tested are paper; regulators ask for testing evidence.
- Global control-plane services (identity, DNS) can be a single dependency even with multi-region.

## Verify
- [ ] Register complete for all ICT arrangements; critical ones flagged.
- [ ] Exit plan for each critical service tested (at least a tabletop and a data export).
