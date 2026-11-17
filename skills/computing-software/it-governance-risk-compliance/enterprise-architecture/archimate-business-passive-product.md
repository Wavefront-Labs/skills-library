---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-business-passive-product
name: archimate-business-passive-product
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-business-passive-product, archimate-business-layer, business object, contract, representation, product, passive structure, access relationship, realization, enterprise-architecture]
level: practitioner
status: draft
description: "Model passive business structure and the Product concept that aggregates services, contracts and interfaces."
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

# Business objects, contracts, representations and products

Goal: model information and offerings.

- Business object: a concept the business cares about; contract: a formal specification; representation: a perceptible form (a report) that realizes an object.
- Product aggregates services and a contract offered to customers.
- Use access relationship from behaviour to object with read, write, readwrite or unspecified access.

Gotchas:
- Distinguish business objects from data objects; the latter belong to the application layer and realize the former.

Verify: each business object accessed by a process is realized by a data object where an application stores it.
