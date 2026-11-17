---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.stakeholder-map
name: stakeholder-map
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, togaf, stakeholder-map, stakeholder-management, concerns-and-viewpoints]
level: practitioner
status: draft
description: "Build a stakeholder map for a cloud architecture engagement: identify, classify by power and interest, capture concerns and pick the views each needs."
sources: ["https://pubs.opengroup.org/togaf-standard/adm-techniques/chap06.html", "https://pubs.opengroup.org/togaf-standard/adm/chap03.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stakeholder map and concerns (Phase A)

## Steps
1. **Identify** broadly: sponsor, business owners, product managers, engineering leads,
   operations/SRE, security, risk and compliance, finance/FinOps, procurement, data
   protection officer, end-user representatives, external regulators and key vendors.
2. **Classify** on a power/interest grid (TOGAF stakeholder management technique):
   - high power, high interest: key players - manage closely;
   - high power, low interest: keep satisfied;
   - low power, high interest: keep informed;
   - low power, low interest: monitor.
3. **Capture concerns** per stakeholder in their words: security wants data residency and
   key control; finance wants predictable spend and capex/opex treatment; operations want
   observability and on-call impact; business wants time to market.
4. **Map concerns to views**: executives get a capability and roadmap view; security gets
   data flow and trust boundaries; operations gets deployment and runbook views; finance
   gets cost model and forecast.
5. **Plan engagement**: cadence, channel and owner per stakeholder group; record in the
   statement of architecture work.
6. Revisit at each phase gate; stakeholders shift when the project moves from design to cutover.

## Gotchas
- Missing the low-visibility veto holders (DPO, works council, enterprise risk) causes late blocks.
- One diagram for everyone satisfies no one.

## Verify
- [ ] Every key player has documented concerns and a view addressing them.
- [ ] Engagement plan agreed with the sponsor.
