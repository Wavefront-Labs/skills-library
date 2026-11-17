---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-contract
name: architecture-contract
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, togaf, architecture-contract, delivery-agreement, phase-g]
level: practitioner
status: draft
description: "Write an architecture contract between architecture and delivery teams or vendors: deliverables, conformance requirements, checkpoints and change handling."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap03.html", "https://pubs.opengroup.org/togaf-standard/adm/chap10.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture contracts

An architecture contract (TOGAF Phase G) is a joint agreement between development partners and
sponsors on the deliverables, quality and fitness-for-purpose of an architecture. It is used
with internal delivery teams and is especially valuable with system integrators.

## Contents
1. Introduction and background; parties and their responsibilities.
2. **Architecture to be implemented**: reference to target architecture, building blocks and
   ADRs; principles and standards that apply.
3. **Conformance requirements**: specific, testable (all data stores private-endpoint only;
   IaC for all resources; tags per policy; DR tested to RTO 4h).
4. **Development phases and checkpoints**: design review, pre-production compliance review,
   post-implementation review.
5. **Deliverables and acceptance criteria** including documentation, runbooks and IaC handover.
6. **Change and dispensation process**: how deviations are requested and approved.
7. **Measures of success and timeline.**
8. **Signatures** of sponsor, architecture authority and delivery lead.

## Steps
- Attach to the statement of work for vendors so conformance is contractual, not advisory.
- Track checkpoints in the governance log; non-conformance triggers the dispensation process.

## Gotchas
- Contracts with vague "follow best practice" clauses are unenforceable.
- Missing handover deliverables (IaC, runbooks) is the most common vendor exit pain.

## Verify
- [ ] Conformance requirements are testable and referenced in the compliance review.
- [ ] Contract signed before build starts.
