---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.ea-organisation-model
name: ea-organisation-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-principles, ea-organisation-model, togaf, preliminary-phase, architecture-team, architecture-capability]
level: practitioner
status: draft
description: "Design the enterprise architecture organisation for cloud: central vs federated architects, roles, reporting lines, decision rights and the team's engagement model."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap02.html", "https://pubs.opengroup.org/togaf-standard/architecture-capability/", "https://learn.microsoft.com/azure/cloud-adoption-framework/organize/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enterprise architecture organisation model and team

## Steps
1. **Pick a model** (TOGAF Preliminary phase defines the organisational model for EA):
   - *Centralised*: one EA team; consistent but a bottleneck at scale.
   - *Federated*: domain/segment architects in business units, a small central team owning
     principles, standards and the repository. Usual answer for cloud at scale.
   - *Embedded*: architects inside product teams, guided by principles and fitness functions.
2. **Define roles**: chief/enterprise architect, domain (business, data, application,
   technology, security) architects, solution architects, cloud platform architect; write
   each role's decisions and deliverables.
3. **Decision rights**: which decisions need the architecture board, which teams decide
   locally within guardrails (ADR + principle compliance), which need security sign-off.
4. **Engagement model**: intake for new initiatives, office hours, design reviews, reusable
   reference architectures; publish the SLA for review turnaround.
5. **Funding and staffing**: size against initiative volume (a common heuristic is one
   solution architect per few product teams); avoid architects without delivery contact.
6. **Measure**: review lead time, reuse of approved patterns, waiver counts.

## Gotchas
- An ivory-tower team producing documents nobody reads; tie output to delivery decisions.
- Federated without shared standards drifts into silos.

## Verify
- [ ] Roles and decision rights published.
- [ ] Engagement model with turnaround targets in use.
