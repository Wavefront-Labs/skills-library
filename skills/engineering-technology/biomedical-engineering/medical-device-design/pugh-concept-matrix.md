---
id: engineering-technology.biomedical-engineering.medical-device-design.pugh-concept-matrix
name: pugh-concept-matrix
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [pugh-matrix, concept-selection, concept-generation, design-methods, trade-study]
level: practitioner
status: draft
description: "Compare device concepts against a datum with Pugh's matrix, iterate by combining best features and avoid common scoring traps before freezing design inputs."
sources: ["Pugh, Total Design: Integrated Methods for Successful Product Engineering", "Ulrich and Eppinger, Product Design and Development (concept selection chapter)", "ISO 14971 (risk as a selection criterion)", "https://www.iso.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pugh concept matrix

**Goal:** narrow 5-15 concepts to 1-2 with a transparent, repeatable comparison, before investing in detailed design.

## Steps
1. **Criteria first.** Take 8-15 selection criteria from the user needs and design inputs (clinical effectiveness, usability, risk, manufacturability, sterilisation compatibility, cost, regulatory path, time to prototype). Include a risk criterion; a concept with an inherent hazard should lose points here, not be fixed later.
2. **Choose a datum.** The existing standard of care device or the best-understood concept. Every other concept is rated against it.
3. **Score** each cell as better (+), same (S) or worse (-) than the datum for that criterion. Use data or a quick test where possible, not opinion alone.
4. **Sum** pluses and minuses (optionally weight criteria by importance, see weighted-decision-matrix).
5. **Iterate.** Take the best concept as the new datum, strip weak features from losers, graft strong features into survivors, rerun. Two or three rounds usually converge.
6. **Record** the matrix, the datum and who scored in the design history file as the rationale for the concept choice.

## Traps
- Criteria that overlap double-count a feature.
- Everyone scoring in a room together anchors on the loudest voice; score independently first, then discuss.
- Sensitivity: change a weight or two cells and check if the winner flips; if it does, the choice is not yet supported and needs a test.
- A matrix cannot rescue missing information; list unknowns and set a learning plan (see feasibility-prototyping).

## Verify
- [ ] Criteria traceable to user needs.
- [ ] Datum stated; scorers independent.
- [ ] Winner survives a sensitivity check.
