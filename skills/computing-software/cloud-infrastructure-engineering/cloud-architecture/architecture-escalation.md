---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-escalation
name: architecture-escalation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, architecture-escalation, togaf, deviation-management, architecture-board]
level: practitioner
status: draft
description: "Escalate architecture deviations found in delivery: severity levels, escalation path and SLAs, decision options (fix, waive, change architecture) and tracking."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap10.html", "https://pubs.opengroup.org/togaf-standard/architecture-capability/chap06.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture deviation escalation

## Steps
1. **Define severity**: critical (security/compliance breach or blocks target state), major
   (non-conformance with significant cost/risk), minor (local deviation, low impact).
2. **Escalation path and timing**: solution architect resolves minor within the team;
   major goes to domain/lead architect within days; critical goes to the architecture board
   (or emergency session) and the sponsor immediately.
3. **Escalation record**: what deviates from which principle/standard/contract clause,
   evidence, impact, options with cost and risk, recommendation, deadline for decision.
4. **Decision options**: remediate now; remediate later with a dated plan; grant a time-boxed
   waiver with compensating controls; or accept that the architecture is wrong and raise an
   architecture change request (Phase H).
5. **Track** in a register; report open escalations and ageing to the board.
6. **Feed back**: recurring deviations against the same standard mean the standard needs work.

## Gotchas
- Escalation seen as punishment drives hiding; frame it as decision support.
- Decisions without a deadline stall delivery; the board must decide within the SLA.

## Verify
- [ ] Severity definitions and SLAs published.
- [ ] Every escalation closed with a recorded decision.
