---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.design-review-milestones
name: design-review-milestones
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, systems-engineering, spacecraft-design, design-reviews, pdr, cdr, srr, entry-exit-criteria]
level: practitioner
status: verified
description: "Plan spacecraft design reviews (SRR, PDR, CDR and others): purpose, entry and exit criteria, and the evidence packages each one needs."
sources:
  - "NASA Systems Engineering Handbook"
  - "NASA NPR 7123.1 (Systems Engineering Processes and Requirements)"
  - "ECSS-M-ST-10C (Project planning and implementation)"
  - "ECSS-M-ST-10C Project planning and implementation: https://ecss.nl/wp-content/uploads/standards/ecss-m/ECSS-M-ST-10C31July2008.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Design review milestones

**Goal:** gate the design at the right maturity with explicit criteria.

## Typical sequence (names vary by agency and programme)
- **MCR/SRR** (NASA names per NPR 7123.1; use the current revision from NODIS)**:** mission concept and system requirements review: requirements are complete, consistent and verifiable; concept feasible.
- **PDR:** preliminary design review: preliminary design meets requirements with acceptable risk; interfaces defined; long-lead items identified.
- **CDR:** critical design review: detailed design complete and ready for fabrication, with verification plans and margins demonstrated.
- **SIR/TRR:** system integration and test readiness reviews.
- **ORR/FRR (FRR/LRR in NASA):** operational readiness and flight readiness reviews.
- ESA projects use PRR (end of phase A), SRR (during phase B), PDR (end of B), CDR (end of C), QR and AR (phase D), ORR, FRR and LRR before launch, then CRR (commissioning) and ELR (end of life), as defined in ECSS-M-ST-10C.

## Procedure
1. Define entry criteria (artifacts complete) and exit criteria (success criteria).
2. Assemble the data package: requirements and verification matrix, trade studies, budgets, interface control documents, risk list, test plans.
3. Run the review with an independent board; record Review Item Discrepancies (RIDs) and actions.
4. Close RIDs before proceeding; document the baseline.

## Gotchas
- A review held without mature requirements validates nothing.
- Open actions at CDR must have owners and dates tied to the build schedule.

## Verify
- [ ] Each criterion has evidence in the data package; RID closure is tracked to completion.
