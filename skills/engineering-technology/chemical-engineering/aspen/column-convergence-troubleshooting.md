---
id: engineering-technology.chemical-engineering.aspen.column-convergence-troubleshooting
name: column-convergence-troubleshooting
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-column-simulation, column-convergence-troubleshooting, convergence, radfrac, column-convergence, troubleshooting, aspen-plus, hysys, initial-estimates, damping]
level: advanced
status: gated
description: "Troubleshoot non-converging RadFrac and HYSYS columns: start from simple specs, use convergence presets, damping, initial estimates and stepwise spec tightening."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Column convergence troubleshooting

**Goal:** a reliable recipe when a column will not converge.

## Escalation ladder
1. **Read the message** in the Control Panel and block history: is it infeasible specs, bad feed, a flash failure in the feed, or just too few iterations?
2. **Check the feed**: convert it to a flash result alone; look for inconsistent compositions, negative flows or a feed that does not satisfy the intended phase state.
3. **Simplify specs**: reflux ratio and distillate rate rather than purities; run and examine the profile.
4. **Increase iterations** (RadFrac default is about 25 (gated: unconfirmed, source is paywalled or blocked)) if Err/Tol is falling steadily but the limit is reached; more iterations will not help when it oscillates or diverges. Then consider two separate settings: the RadFrac **algorithm** (AspenTech's Aspen Plus study guide lists Sum-Rates, Non-ideal and Newton as alternatives to the default, each suited to particular columns) and the **initialization method** matched to the mixture (the same guide confirms RadFrac initialization methods exist; option names such as Standard, Petroleum/Wide-boiling, Strongly non-ideal liquid and Azeotropic vary with version (gated: unconfirmed, source is paywalled or blocked)). An earlier version of this skill mixed the two.
5. **Provide initial estimates**: temperature profile, vapour/liquid flows, or use the previous converged solution; restart from the last good case.
6. **Move specs in steps**: tighten the target gradually (distillate purity from 90% to 95% to 99%), re-running each time.
7. **Check physical feasibility**: purity requested exceeds the number of stages or crosses an azeotrope or distillation boundary.
8. **Damping or Newton settings** only after the above; changing them blindly can hide a true infeasibility.

## HYSYS notes
Use the Monitor to watch the heat and spec errors; the active spec set must equal the degrees of freedom; use Reset or re-run from initial estimates.

## Gotchas
- A column can converge to a trivial or non-physical solution (all liquid, zero reflux); look at the profile.
- Mixed feeds with water may need a three-phase configuration.

## Verify
- [ ] Final solution passes physical sense checks: smooth profiles, positive flows, purity targets met.
- [ ] The steps that fixed it are recorded in the case notes.
