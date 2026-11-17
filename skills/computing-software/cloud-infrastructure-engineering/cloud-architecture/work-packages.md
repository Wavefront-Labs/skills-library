---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.work-packages
name: work-packages
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-planning, transition-architecture, togaf, work-packages, dependency-sequencing, implementation-and-migration-plan]
level: practitioner
status: draft
description: "Group gaps into work packages, analyse dependencies, estimate and sequence them into an implementation and migration plan with clear owners."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap08.html", "https://pubs.opengroup.org/togaf-standard/adm/chap09.html", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap11.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Work packages and dependency sequencing

## Steps
1. **Consolidate gaps** from all domains into a list; group related ones into work packages
   that a single team or programme can deliver (e.g. "Central identity federation",
   "Migrate billing app and its database").
2. **Describe each package**: objective, gaps closed, deliverables, owner, estimate (range),
   prerequisites, business value, risks.
3. **Dependency analysis** (TOGAF Phase E technique): business, data, application and
   technology dependencies. Build a dependency graph; anything with many dependants is a
   foundation package and goes first.
4. **Prioritise**: value, risk, dependencies, effort; use a simple scoring or cost of delay.
5. **Sequence into the transition architectures**; check resource contention (same
   specialists needed in parallel).
6. **Produce the implementation and migration plan** (Phase F): timeline, funding,
   milestones, governance checkpoints.

## Gotchas
- Packages organised by technology layer (all networking, then all compute) delay value;
  prefer vertical slices delivering a working workload.
- Hidden shared dependencies (a single DBA, a firewall change board) gate many packages.

## Verify
- [ ] Dependency graph has no cycles and foundations are scheduled first.
- [ ] Each package has an owner and acceptance criteria.
