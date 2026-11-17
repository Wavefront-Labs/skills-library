---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gap-analysis
name: gap-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-planning, transition-architecture, togaf, gap-analysis, baseline-target]
level: practitioner
status: draft
description: "Run a TOGAF gap analysis between baseline and target cloud architecture: building-block matrix, new, retained and eliminated items, and resulting work."
sources: ["https://pubs.opengroup.org/togaf-standard/adm-techniques/chap12.html", "https://pubs.opengroup.org/togaf-standard/adm/chap07.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gap analysis: baseline vs target

## Steps
1. **List building blocks** of the baseline (rows) and target (columns) for one domain at a
   time: business, data, application, technology.
2. **Fill the matrix** (TOGAF gap analysis technique):
   - block in both: **included** (possibly changed - note how);
   - baseline only: **eliminated** - intended (decommission) or accidental (a gap: lost function);
   - target only: **new** - must be built, bought or configured.
   Add a final "eliminated" column and "new" row so every block lands somewhere.
3. **Check for accidental omissions**: functions in the baseline not provided by any target
   block - batch jobs, reports, interfaces nobody documented. Interview operators.
4. **Characterise each gap**: size, dependencies, risk, owner.
5. **Consolidate across domains** in Phase E: a new technology block may be needed by several
   application gaps; combine into one work item.
6. Feed gaps into work packages and the roadmap.

## Gotchas
- Baselines built from documentation miss the undocumented integrations; validate against
  network flow and job scheduler data.
- Data gaps (history, archives) are the most commonly forgotten.

## Verify
- [ ] Every baseline block is marked included or eliminated with reason.
- [ ] Every gap has an owner and a work package reference.
