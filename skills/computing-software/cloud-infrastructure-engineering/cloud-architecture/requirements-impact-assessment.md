---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.requirements-impact-assessment
name: requirements-impact-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, requirements-impact-assessment, togaf, requirements-management, change-impact]
level: practitioner
status: draft
description: "Assess the impact of a new or changed requirement on the architecture: trace to building blocks, classify the change, estimate effort and decide the ADM re-entry point."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap12.html", "https://pubs.opengroup.org/togaf-standard/adm/chap11.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Requirements impact assessment

## Steps
1. **Register the requirement** with source, rationale, priority and stakeholders (TOGAF
   Requirements Management runs through every phase).
2. **Trace impact**: use traceability links (requirement to principle, building block,
   application, data entity, technology) to list everything touched.
3. **Assess**: effect on current and target architectures, transition architectures,
   in-flight projects, architecture contracts, cost and timeline, and conflicts with other
   requirements.
4. **Classify** (Phase H): simplification, incremental change (handled within the current
   architecture), or re-architecting change (new ADM cycle).
5. **Decide re-entry point**: which phase to revisit (e.g. a new residency law re-enters at
   Phase D technology and F planning).
6. **Record the decision** in the requirements impact statement, update the repository and
   notify affected projects.

## Gotchas
- Without traceability links, impact assessment becomes guesswork; build them as you go.
- Small requirements can conflict with principles; check principles first.

## Verify
- [ ] Impact statement lists affected building blocks and projects.
- [ ] Classification and re-entry decision recorded.
