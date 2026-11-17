---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-debt
name: architecture-debt
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, togaf, architecture-debt, technical-debt-register, phase-h]
level: practitioner
status: draft
description: "Keep an architecture technical-debt register: capture, quantify interest, prioritise against roadmap work and fund repayment."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap11.html", "https://martinfowler.com/bliki/TechnicalDebtQuadrant.html", "https://learn.microsoft.com/azure/well-architected/operational-excellence/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture technical-debt register

Architecture debt is structural: deprecated runtimes, single-region designs that should be
multi-AZ, point-to-point integrations, expired waivers, unsupported building blocks. It is
larger and slower to repay than code debt.

## Register fields
ID, description, affected systems, origin (deliberate trade-off, waiver, drift, ageing),
**principal** (effort to fix), **interest** (ongoing cost: incidents, toil hours, licence
premiums, extended support fees, blocked features, risk exposure), owner, target date, status.

## Steps
1. **Capture** from ADR consequences, expired waivers, compliance findings, incident
   reviews, end-of-life tracking and engineer surveys.
2. **Quantify interest** in money or hours per quarter where possible; risk items by
   likelihood x impact.
3. **Prioritise** by interest / principal ratio and by roadmap dependency (debt that blocks
   a planned transition goes first).
4. **Fund repayment**: a fixed capacity share (e.g. 15-20% per team) or explicit roadmap
   items for large debts; report repayment as outcomes (incidents avoided, cost removed).
5. **Review quarterly** at the architecture board; reassess interest as conditions change.

## Gotchas
- A register nobody funds becomes a guilt list.
- Not all debt needs repaying; retiring the system can be cheaper.

## Verify
- [ ] Top 10 items have quantified interest and an owner.
- [ ] Repayment capacity tracked against plan each quarter.
