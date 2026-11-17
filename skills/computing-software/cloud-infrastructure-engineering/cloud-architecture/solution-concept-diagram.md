---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.solution-concept-diagram
name: solution-concept-diagram
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, solution-concept-diagram, togaf-phase-a, high-level-diagram, executive-diagram, context-diagram]
level: intro
status: draft
description: "Draw a one-page solution concept diagram for the architecture vision: actors, key capabilities, major components and external systems, readable by executives in a minute."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://c4model.com/diagrams/system-context"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Solution concept diagram

The TOGAF Phase A solution concept diagram is a high-level orientation of the solution: the
"napkin" picture the sponsor signs off.

## Content
- Actors (customers, staff roles, partners) at the edges.
- The new or changed capabilities in the centre, grouped by business meaning, not by AWS icon.
- Major components / platforms (e.g. "Customer portal", "Event platform", "Data platform").
- External systems and key data flows labelled with what moves (orders, identity, payments).
- Optionally colour: new / changed / retained / retired.

## Rules
- One page, no more than ~15 boxes, plain shapes with a legend.
- Vendor product names only where they are decided and matter to the audience.
- Title, date, version, author, status (draft/approved).
- Avoid detailed network or IP information; that belongs to Phase D views.

## Steps
1. Start from the stakeholder concerns and business drivers.
2. Sketch with the sponsor and a domain expert in a 30-minute session.
3. Validate: can a non-technical exec explain the solution back from the picture?
4. Store in the repository; reference it from the Statement of Architecture Work.

## Verify
- [ ] Sponsor can narrate it unaided.
- [ ] Every element traces to a driver or requirement.
