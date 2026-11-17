---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.technology-nonfunctional-capacity
name: technology-nonfunctional-capacity
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [technology-nonfunctional-capacity, adm-phase-d-technology, non functional requirements, availability, rto, rpo, capacity planning, scalability, resilience, enterprise-architecture]
level: advanced
status: draft
description: "State availability, performance, scalability, recovery and security targets for the technology architecture in measurable terms."
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

# Non-functional requirements, capacity and resilience

Goal: turn qualities into numbers the technology architecture can be tested against.

- Availability: target percentage and measurement window; derive redundancy.
- Recovery: RTO and RPO per business service, tied to the business continuity plan.
- Performance: response time at percentile under stated load.
- Capacity: growth assumptions over 3 years; headroom policy.
- Security: zoning, identity, encryption standards, logging.

Gotchas:
- A single availability figure hides dependency chains; multiply along the path.
- Unstated assumptions about cloud region failure.

Verify: each target has a metric, a threshold and a test or monitor.
