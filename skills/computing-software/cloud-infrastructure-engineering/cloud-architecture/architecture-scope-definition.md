---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-scope-definition
name: architecture-scope-definition
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, architecture-scope-definition, togaf, phase-a, scope]
level: practitioner
status: draft
description: "Define architecture scope in TOGAF Phase A: breadth, depth, time period and architecture domains, plus explicit exclusions and constraints, before any design work."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap03.html", "https://pubs.opengroup.org/togaf-standard/adm/chap02.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defining architecture scope

## Steps
1. **Breadth**: which business units, products, geographies and systems are in. Name them.
2. **Depth**: level of detail (strategic, segment, capability or solution architecture).
   Strategic work needs no physical design; solution work does.
3. **Time period**: the horizon for the target state and the transition architectures in
   between (for cloud often 18-36 months with 6-12 month plateaus).
4. **Architecture domains**: business, data, application, technology; say which are in and
   at what depth (a lift-and-shift may be mostly technology; a modernisation touches all).
5. **Exclusions and constraints**: what is explicitly out, fixed decisions (provider already
   chosen, budget, regulatory dates), assumptions to validate.
6. **Confirm with sponsor** in the Statement of Architecture Work; changes to scope go
   through the same approval.

## Gotchas
- Unbounded breadth with solution-level depth is how architecture work never finishes.
- Unstated exclusions return as surprise requirements in Phase F.

## Verify
- [ ] Breadth, depth, time and domains each stated in writing.
- [ ] Sponsor-approved exclusions list.
