---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.application-inventory-data
name: application-inventory-data
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [application-inventory-data, application-portfolio-rationalisation, application inventory, application catalog, apm data, cost per application, usage data, lifecycle, cmdb, enterprise-architecture]
level: practitioner
status: draft
description: "Create an authoritative application inventory with owners, cost, usage, technology and lifecycle data."
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

# Build the application inventory and collect data

Goal: reliable inputs for rationalisation.

- Sources: CMDB, procurement, SSO logs, cloud bills, interviews.
- Fields: name, description, owner, business capability, users, cost, technology stack, vendor, support end, data classification, hosting.
- Reconcile duplicates and shadow IT.
- Assign a data steward and refresh cadence.

Gotchas:
- Cost allocation is contentious; agree the method first.

Verify: 95 percent of records have owner, cost and lifecycle fields.
