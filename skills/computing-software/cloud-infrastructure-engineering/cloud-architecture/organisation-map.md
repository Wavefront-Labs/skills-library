---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.organisation-map
name: organisation-map
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, organisation-map, togaf, phase-b, actor-catalogue, role-catalogue]
level: practitioner
status: draft
description: "Produce a TOGAF organisation map plus actor and role catalogues: units, locations, relationships, and who performs which business functions in the cloud change."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap04.html", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://www.businessarchitectureguild.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Organisation map and actor / role catalogue

## Steps
1. **Organisation map**: business units, their relationships (reporting, partnering, service
   provision), and external parties (customers, suppliers, regulators). Keep it at unit level;
   it is not the HR org chart.
2. **Organisation/actor catalogue**: each actor (person type, unit, system acting as a party)
   with its unit and location.
3. **Role catalogue**: roles (e.g. claims handler, platform engineer, data steward) separate
   from people; a person can hold several roles.
4. **Link to capabilities and value streams**: which unit owns each capability, which roles
   perform each value-stream stage. This exposes duplicate ownership and gaps.
5. **Use it for cloud change**: identify units affected by migration, who loses or gains
   responsibilities (e.g. infrastructure team to platform team), training needs and RACI.
6. **Store in the repository** with owners so it stays current after reorgs.

## Gotchas
- Mapping people instead of roles goes stale at the next reorg.
- External actors are often forgotten; regulators and partners have interfaces too.

## Verify
- [ ] Map, actor and role catalogues cross-referenced to capabilities.
- [ ] Impacted units and role changes listed for the transition.
