---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-work-package-plateau-gap
name: archimate-work-package-plateau-gap
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-work-package-plateau-gap, archimate-implementation-migration, work package, deliverable, implementation event, plateau, gap, migration, transition architecture, enterprise-architecture]
level: practitioner
status: draft
description: "Model change with work packages, deliverables, implementation events, plateaus and gaps."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Work package, deliverable, implementation event, plateau and gap

Goal: represent roadmaps in the model.

- Work package: a series of actions with a goal; deliverable: a result; implementation event: a state change related to implementation.
- Plateau: a relatively stable architecture state; gap: difference between two plateaus.
- Relationships: work package realizes deliverable, deliverable realizes plateau or core elements; plateau triggers next plateau; gap associated with two plateaus.

Gotchas:
- Model only the plateaus you plan; baseline and target plus transitions.

Verify: every target element is realized by a deliverable.
