---
id: engineering-technology.biomedical-engineering.medical-device-design.weighted-decision-matrix
name: weighted-decision-matrix
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [decision-matrix, concept-selection, concept-generation, weighted-scoring, ahp, trade-study, sensitivity-analysis]
level: practitioner
status: draft
description: "Score concepts with a weighted decision matrix: criteria weights, 1-5 scales with anchors, normalisation, sensitivity analysis and avoiding false precision."
sources: ["Ulrich and Eppinger, Product Design and Development (concept selection)", "Saaty, The Analytic Hierarchy Process", "Pahl and Beitz, Engineering Design"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Weighted decision matrix

**Goal:** a transparent numerical comparison of concepts that survives a sensitivity check.

## Steps
1. **Criteria:** 6-12 criteria derived from user needs and constraints (clinical effect, safety margin, usability, sterilisation compatibility, manufacturability, unit cost, time to market, regulatory evidence burden, IP).
2. **Weights:** give each criterion a weight so they sum to 100% (or 1.0). Use pairwise comparison or AHP when the team disagrees; document who set the weights.
3. **Rating scale with anchors:** use 1-5 and define what each score means for each criterion with measurable anchors (for cost: 5 = below target, 1 = above 150% of target).
4. **Score** each concept per criterion, ideally independently by several people; average and note variance.
5. **Compute** weighted score = sum of (weight x score).
6. **Sensitivity:** vary each weight by plus or minus 50% and see if the ranking changes; if the winner flips, the choice depends on a contested weight, and needs more data or a test.
7. **Gate criteria:** do not let high scores on convenience offset a failing score on safety; use pass/fail gates for must-have criteria before the matrix.

## Traps
- False precision (a 3.47 versus 3.52 difference is noise).
- Overlapping criteria that double count.
- Anchoring on one champion's preferred concept; hide names during scoring.

## Verify
- [ ] Weights sum to 100% and rationale recorded.
- [ ] Anchors written for each criterion.
- [ ] Sensitivity table in the record.
