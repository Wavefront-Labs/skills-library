---
id: engineering-technology.chemical-engineering.separation-processes.extractor-stage-calculation
name: extractor-stage-calculation
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-liquid-extraction, extractor-stage-calculation, extraction-stages, extraction-factor, countercurrent-extraction, crosscurrent-extraction, difference-point, minimum-solvent-ratio, solvent-to-feed-ratio]
level: practitioner
status: draft
description: "Calculate extraction stages for cross-current and countercurrent contact, extraction factor, minimum solvent and graphical difference-point construction."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extractor stage calculation and solvent ratio

**Goal:** number of stages and solvent flow for a target raffinate concentration.

## Dilute immiscible case (Kremser form)
Extraction factor E = K S/F (K = distribution coefficient in mass or mole ratio form; S solvent flow, F feed). For countercurrent contact with solvent free of solute entering:
(x_0 - x_N)/x_0 = (E^(N+1) - E)/(E^(N+1) - 1) (E not equal to 1)
so N follows from the required recovery. Cross-current contact with fresh solvent per stage: x_N = x_0/(1 + K S_i/F)^N for equal splits.
Countercurrent contact is far more efficient than cross-current for the same solvent total.

## Partially miscible systems (graphical)
1. Locate F, S on the ternary diagram, find M.
2. Raffinate product R_N from the target composition; extract E_1 from the line through R_N and M.
3. **Difference point** Delta = E_1 - F = R_N - S (intersection of lines F E_1 and S R_N, often outside the triangle).
4. Step off stages: tie line to get R_1 from E_1; line from Delta through R_1 to find E_2; repeat until the raffinate composition reaches or passes R_N.

## Minimum solvent
When a tie line passes through the feed point, the stage count becomes infinite: S_min. Operate at 1.3 to 2 times S_min (check economics, including solvent recovery cost).

## Gotchas
- Stage efficiency in real extractors often well below 100%; set by HETS (height equivalent to a theoretical stage) from vendor or pilot data.
- Solvent recovery (distillation) often dominates the cost.

## Verify
- [ ] Overall mass and solute balances close.
- [ ] Check the result with a rigorous LLE model in a simulator.
