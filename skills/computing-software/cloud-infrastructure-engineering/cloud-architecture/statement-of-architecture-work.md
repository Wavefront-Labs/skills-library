---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.statement-of-architecture-work
name: statement-of-architecture-work
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, togaf, statement-of-architecture-work, architecture-scope, phase-a]
level: practitioner
status: draft
description: "Write a TOGAF statement of architecture work for a cloud initiative: scope, stakeholders, approach, deliverables, plan, risks and sign-off."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap03.html", "https://pubs.opengroup.org/togaf-standard/adm/chap03.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statement of architecture work

The statement of architecture work (SoAW) is the Phase A contract between the architecture
team and the sponsor: what will be architected, how and by when.

## Contents (TOGAF outline, trimmed)
1. **Title, sponsor, request for architecture work reference.**
2. **Background and drivers** - one page, link to business outcomes.
3. **Scope**: breadth (business units, workloads, regions), depth (strategic vs
   solution-level), time horizon, architecture domains in scope (business, data,
   application, technology), and explicit **out of scope**.
4. **Stakeholders and concerns** - summary of the stakeholder map.
5. **Approach**: ADM tailoring used, phases and iterations, frameworks and reference models.
6. **Deliverables**: e.g. target architecture, gap analysis, roadmap, landing-zone design,
   ADRs; format and acceptance criteria for each.
7. **Plan and resources**: milestones, people, effort.
8. **Risks, assumptions and constraints** (budget ceiling, mandated provider, fixed exit date).
9. **Acceptance and sign-off**: who approves deliverables and how changes to scope are handled.

## Steps
- Draft after initial stakeholder interviews; review with key players; get the sponsor to
  sign before detailed design.
- Treat scope changes as change requests against the SoAW, with impact on plan and cost.

## Gotchas
- Vague scope ("modernise the platform") guarantees scope creep.
- No acceptance criteria means deliverables are never formally done.

## Verify
- [ ] Out-of-scope list present and sponsor-signed.
- [ ] Each deliverable has acceptance criteria and approver.
