---
id: engineering-technology.aerospace-engineering.aircraft-structures.cmh-17-composite-allowables
name: cmh-17-composite-allowables
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [cmh-17, composite-allowables, a-basis, b-basis, statistical-allowables, aerospace-materials]
level: practitioner
status: verified
description: "Generate and use composite material allowables from CMH-17 procedures, including A- and B-basis definitions, batch structure, and environmental knockdowns."
sources:
  - "CMH-17 Composite Materials Handbook (Volume 1 and 3)"
  - "FAA 14 CFR 25.613"
  - "https://www.law.cornell.edu/cfr/text/14/25.613"
  - "https://www.law.cornell.edu/cfr/text/14/25.613"
  - "https://www.cmh17.org/"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# CMH-17 composite allowables

**Goal:** statistically defensible design values for composite materials.

## What CMH-17 is
The Composite Materials Handbook (CMH-17, formerly MIL-HDBK-17) is a multi-volume reference. Volume numbering and scope below are (gated: unconfirmed, source is paywalled or blocked). Volume 1 covers guidelines for characterisation of structural materials (test planning, statistics), Volume 2 gives polymer matrix material property data, Volume 3 covers usage, design and analysis, and other volumes cover metal matrix, ceramic matrix and sandwich structure. Check the current edition.

## Basis definitions
- **A-basis**: value above which at least 99 percent of the population is expected to fall with 95 percent confidence.
- **B-basis**: at least 90 percent of the population with 95 percent confidence.
- 14 CFR 25.613(a) requires design values established on a statistical basis from enough tests of material meeting approved specifications; 25.613(b) selects the probability: 99 percent with 95 percent confidence where loads pass through a single member whose failure would lose structural integrity (A-basis level), and 90 percent with 95 percent confidence for redundant structure (B-basis level). 25.603 requires approved material specifications. Confirm means of compliance with your authority.

## Procedure
1. Plan a test matrix with several independent batches (the handbook sets minimum batches and specimens per condition) in the relevant environments (room temperature dry, elevated temperature wet, cold dry).
2. Test per the standard methods chosen in the plan, record failure modes.
3. Check batch-to-batch variation (ANOVA or Anderson-Darling k-sample tests) to decide whether data pool.
4. Compute basis values by the handbook method (normal, Weibull or nonparametric as the data demand, or the modified coefficient-of-variation approach for small data sets).
5. Document and have the values accepted by the programme's material board.

## Gotchas
- Allowables are valid only for the same material, process and specification; process changes require equivalence testing.
- Data in the handbook are proprietary to their sources; use for guidance and cite correctly.

## Verify
- [ ] Each basis value comes with sample size, batch count, distribution used and condition.
