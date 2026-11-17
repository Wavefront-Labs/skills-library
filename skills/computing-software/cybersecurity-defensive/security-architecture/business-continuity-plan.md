---
id: computing-software.cybersecurity-defensive.security-architecture.business-continuity-plan
name: business-continuity-plan
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [business-continuity-plan, bcp, iso-22301, business-impact-analysis, continuity-strategy, plan-exercising, nist-sp-800-34]
level: practitioner
status: draft
description: "Write and exercise a business continuity plan: BIA-driven priorities, continuity strategies per resource loss, activation criteria, roles, workarounds and test cycles."
sources: ["https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final", "https://www.iso.org/standard/75106.html", "https://www.ready.gov/business/emergency-plans/continuity-planning"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business continuity plan

A BCP keeps critical business functions running when people, premises, technology or suppliers are
lost. A DR plan restores IT; the BCP covers the business while IT is down.

## Inputs
- BIA: critical activities, maximum tolerable period of disruption (MTPD), RTO/RPO, dependencies (people, sites, apps, suppliers). See `computing-software.cybersecurity-defensive.security-architecture.rto-rpo-and-business-impact-analysis`.

## Plan structure (per business unit)
1. Scope and objectives.
2. Activation criteria and authority (who declares, thresholds).
3. Roles and contact tree (with deputies; offline copy).
4. Strategies by loss scenario:
   | Loss | Strategy |
   |---|---|
   | Site | Work from home, alternate site, reciprocal agreement |
   | IT systems | Manual workarounds (paper forms, offline price lists), DR failover |
   | People | Cross-training, documented procedures, succession |
   | Supplier | Secondary supplier, stock buffer, contractual exit plan |
   | Cyber (ransomware) | Out-of-band comms, clean device pool, pre-approved decision to isolate |
5. Recovery and return-to-normal steps (back-loading manual transactions).
6. Appendices: call lists, vital records locations, supplier contacts.

## Exercising
- Annual tabletop per plan, scenario-based (ransomware with AD down is the most revealing).
- Periodic call-tree tests and a live workaround test for top processes.
- Record lessons and update the plan; version and owner on the cover.

## Gotchas
- Plans stored only on the file server that is encrypted are useless; keep printed/offline copies.
- Manual workarounds that nobody has practised fail at volume.
- Contact lists go stale within months.

## Verify
- [ ] Every critical activity in the BIA has a strategy and owner.
- [ ] Exercise held in the last 12 months with actions closed.
