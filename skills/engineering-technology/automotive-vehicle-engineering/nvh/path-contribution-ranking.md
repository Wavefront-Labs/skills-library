---
id: engineering-technology.automotive-vehicle-engineering.nvh.path-contribution-ranking
name: path-contribution-ranking
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [path-contribution, contribution-analysis, contribution-ranking, nvh-troubleshooting, countermeasure, path-ranking]
level: practitioner
status: draft
description: "Rank source and path contributions in dB and phase, pick the countermeasure target, predict the benefit by what-if modification and verify in the vehicle."
sources:
  - "Harrison, Vehicle Refinement"
  - "Plunt, Finding and fixing vehicle NVH problems with TPA"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Path contribution ranking

1. Plot contributions vs order or frequency in dB for each path; mark the problem frequency or order and list paths within 6 dB of the largest.
2. Check phase between top paths: out-of-phase pairs cancel and are fragile; if one is reduced the total can rise. Computed example: two paths of amplitude 1.0 and 0.9 in antiphase sum to -20 dB re 1; cutting the 0.9 path by 6 dB raises the total to -5.2 dB, about 15 dB worse.
3. Decide what is cheap and effective: reduce force (softer mount, balance, tuning), reduce transfer (stiffer body locally, damping), or reduce the source (engine balance, tyre).
4. What-if: scale a path force or transfer function by the proposed change (e.g. 6 dB lower mount stiffness) and recompute the sum; evaluate the total effect, including cross-effects.
5. Plan verification: build the modification and measure the same operating condition again; compare in the same units.
6. Document the contributions before and after, the cost and mass of the change.
7. Iterate: the next path then dominates; stop at the target level.

**Gotchas:** fixing a path that only contributes at a different order.

## Verify
- [ ] Predicted vs measured improvement within about 2 dB.
- [ ] Before/after contribution plots archived with test conditions.
