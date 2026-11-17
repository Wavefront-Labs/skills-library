---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.transformation-readiness
name: transformation-readiness
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, transformation-readiness, togaf-phase-a, readiness-factors, change-readiness, maturity-rating]
level: practitioner
status: draft
description: "Run a TOGAF business transformation readiness assessment for a cloud programme: readiness factors, maturity ratings, risks and actions feeding the architecture vision."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap03.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap06.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business transformation readiness assessment

## Readiness factors (TOGAF technique; adapt names)
Vision, desire/willingness/resolve, need, business case, funding, sponsorship and leadership,
governance, accountability, workable approach and execution model, IT capacity to execute,
departmental capacity to execute, ability to implement and operate. Add cloud-specific: skills,
security/compliance approval path, vendor contracts, data readiness.

## Steps
1. Workshop with sponsor, business and IT leads; for each factor agree current maturity (e.g.
   0 = absent to 5 = optimised), target, and how urgent the gap is.
2. Plot factors on a readiness/importance grid; anything important and low is a risk.
3. For each risk write an action: training, hiring, contract change, governance setup, pilot.
4. Feed into Phase A outputs: risks in the vision, actions in the Statement of Architecture Work,
   and later into the migration plan (Phase F).
5. Reassess at each major gate.

## Cloud examples
- Funding: capex approval process cannot handle variable opex -> FinOps/finance action.
- IT capacity: no one has run production on the target cloud -> partner or training first.
- Departmental capacity: business cannot staff UAT for migration waves -> resequence waves.

## Gotchas
- Self-assessment optimism; ask for evidence (e.g. certified staff count, approved policies).
- Doing the assessment and filing it. The actions must be tracked like project work.

## Verify
- [ ] Every factor rated with evidence and an owner.
- [ ] Actions appear in the plan with dates.
