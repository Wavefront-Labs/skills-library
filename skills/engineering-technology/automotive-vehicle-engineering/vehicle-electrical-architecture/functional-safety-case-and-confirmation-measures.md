---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.functional-safety-case-and-confirmation-measures
name: functional-safety-case-and-confirmation-measures
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [safety-case, confirmation-measures, safety-assessment, gsn, safety-plan, dia, iso-26262-part-2, functional-safety]
level: practitioner
status: gated
description: "Build the safety case and plan confirmation measures: argument structure, evidence index, reviews, audits, assessment independence and release for production."
sources:
  - "ISO 26262-2:2018 (management of functional safety) and ISO 26262-10; confirm edition and assessor requirements"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Safety case and confirmation measures

Professional practice guidance; the project's safety manager and independent assessor decide what is required.

1. **Safety plan:** activities, responsibilities, tailoring decisions, work products, schedule; updated through the project.
2. **Safety case:** a structured argument that safety goals are met: claims, argument, evidence; commonly shown with Goal Structuring Notation (GSN). Top claim: the item is acceptably safe; sub-claims for requirements, hazard analysis, design, verification, production, field monitoring.
3. **Evidence index:** link each claim to documents (HARA, safety concept, FMEDA, test reports, tool qualification).
4. **Confirmation measures:** confirmation reviews (of work products), functional safety audits (of process), and functional safety assessment (of the item); independence required depends on ASIL (more independent for higher ASIL, as defined in ISO 26262-2 (gated: unconfirmed, source is paywalled or blocked)).
5. **DIA (development interface agreement):** responsibilities and work products between OEM and suppliers; defines who does HARA, safety analyses, and shared evidence.
6. **Release for production:** based on the safety case, assessment report, completed verification and open-issue analysis.
7. **Field monitoring:** process for field issues and updates.

**Gotchas:** safety case written at the end; evidence not traceable to versions.

## Verify
- [ ] Every top-level claim has linked evidence with versions.
- [ ] Assessment findings closed or justified before release.
