---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-business-application-alignment
name: archimate-business-application-alignment
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-business-application-alignment, archimate-application-layer, business application alignment, application supports process, serving relationship, realization, automation, data object realizes business object, enterprise-architecture]
level: practitioner
status: draft
description: "Show how applications support business through serving, realization of business processes and data objects realizing business objects."
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

# Business and application alignment relationships

Goal: link business process to supporting applications.

- Application service serves a business process or actor.
- Application process or function may realize a business process or function when the process is fully automated.
- Data object may realize a business object.
- Use layered viewpoint for the picture and the Business Process Cooperation viewpoint for detail.

Gotchas:
- Do not draw the application as a user of the business process; the direction is serving from application to business.

Verify: every business process has at least one serving application service or an explicit manual flag.
