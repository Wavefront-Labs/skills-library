---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.requirements-traceability
name: requirements-traceability
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, togaf, requirements-traceability, requirements-management, traceability-matrix]
level: practitioner
status: draft
description: "Maintain requirements traceability through the ADM: link requirements to decisions, building blocks, tests and changes, and assess change impact."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap12.html", "https://www.iso.org/standard/72089.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Requirements traceability

TOGAF requirements management sits at the centre of the ADM: requirements are identified,
stored and fed into and out of every phase. Traceability is what lets you answer "what breaks
if this changes?" and "why is it built this way?".

## Steps
1. **Single requirements repository** with IDs: business, functional, non-functional,
   regulatory, constraints. Each has source, owner, priority, status.
2. **Trace links** (a matrix or tool links): requirement -> ADRs -> building blocks /
   components -> tests (load test, DR drill, policy check) -> work packages.
3. **Change intake**: new or changed requirement triggers impact assessment - which
   decisions, components and tests are affected, and does it need a new ADM cycle (Phase H
   classifies changes as simplification, incremental, or re-architecting).
4. **Verify coverage**: every high-priority requirement has at least one test; every
   component traces to at least one requirement (else question why it exists).
5. **Report**: requirement status and test results per release; regulators often ask for this.

## Gotchas
- Spreadsheets of links go stale; keep IDs in ADRs, tickets and tests so links are searchable.
- Over-tracing trivial requirements wastes effort; trace NFRs, regulatory and high-risk items.

## Verify
- [ ] Each regulatory requirement links to a control and evidence.
- [ ] Change requests include an impact assessment referencing requirement IDs.
