---
id: computing-software.it-governance-risk-compliance.iso-27001-isms.iso-scope-boundary
name: iso-scope-boundary
category: computing-software
field: it-governance-risk-compliance
product: iso-27001-isms
tags:
- iso-27001-isms
- iso-scope-boundary
level: practitioner
status: draft
description: 'Define and document the ISMS scope per clause 4.3: organisational units, locations, assets, interfaces and dependencies, with justified exclusions.'
sources:
- https://www.iso.org/standard/27001
- https://www.iso.org/standard/75652.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISMS scope statement and boundaries (4.3)
**Goal:** a scope statement an auditor can test against the real estate.
- Scope must consider 4.1 issues, 4.2 requirements, and interfaces and dependencies between activities done by the organisation and by others.
- Write it as: products/services, business units, sites, systems/networks, cloud and outsourced providers in or out, with a boundary diagram.
- Scope is documented information; the certificate wording derives from it.
- Exclusions of individual Annex A controls belong in the SoA, not the scope; scope exclusions need rationale and must not undermine assurance.

## Gotchas
- Scoping out the system holding customer data while certifying the rest invites rejection by customers and auditors.
- Shared services (HR, IT, cloud) used by in-scope teams are interfaces: list them.

## Self-check
Trace one in-scope process end to end and confirm every system, site and supplier it touches is in scope or listed as an interface.
