---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-roadmap
name: architecture-roadmap
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-planning, transition-architecture, togaf, architecture-roadmap, transition-states]
level: practitioner
status: draft
description: "Build an architecture roadmap with transition architectures: plateau definitions, sequencing, value at each state, and keeping it current."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap08.html", "https://pubs.opengroup.org/togaf-standard/adm/chap09.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap11.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture roadmap and transition states

## Steps
1. **Define transition architectures** (plateaus) between baseline and target: stable,
   operable states that each deliver business value, e.g.
   T1 landing zone and first 20 workloads rehosted; T2 data platform on managed services and
   datacentre A closed; T3 core platform refactored, datacentre B closed.
2. **Each state must be safe to stop at**: if funding stops after T1, the estate is still
   supportable.
3. **Sequence** using dependencies (landing zone before workloads, identity before
   everything), business priorities and value, risk (low-risk first to build skills),
   constraints (contract end dates, hardware refresh).
4. **Show it on one page**: swimlanes per domain, transitions as milestones, work packages
   as bars, key decisions and dependencies marked.
5. **State the value per transition** (outcome metric expected) so progress is measured by
   outcomes, not tasks.
6. **Review every planning increment**; re-baseline when assumptions change and record why.

## Gotchas
- Roadmaps with only a start and target state hide a long, risky middle.
- Hard dates for distant transitions create false precision; use quarters or ranges.

## Verify
- [ ] Each transition has defined architecture, value and exit criteria.
- [ ] Roadmap version and change log maintained.
