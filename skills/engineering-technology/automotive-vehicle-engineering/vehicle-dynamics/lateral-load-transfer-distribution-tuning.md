---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.lateral-load-transfer-distribution-tuning
name: lateral-load-transfer-distribution-tuning
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [lltd, load-transfer-distribution, balance-tuning, understeer-tuning, roll-stiffness-ratio, handling-balance]
level: practitioner
status: draft
description: "Tune handling balance with lateral load transfer distribution: choose the front share relative to weight distribution and adjust via bars, springs and roll centres."
sources:
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# LLTD tuning

1. Compute LLTD (front share of total transfer) with the lateral-load-transfer calculation including geometric and unsprung contributions.
2. Principle: raising front LLTD adds understeer; reducing it adds oversteer, via tyre load sensitivity (see tyre-load-sensitivity). For a front-drive road car the front share is generally set above the front weight fraction for stable understeer; sports cars sit closer. Confirm with test on your tyres.
3. Levers, in order of side effects: anti-roll bar rates (cheapest to change), spring rates (also affect ride), roll centre heights (affect jacking and camber), tyre pressures/sizes (stiffness and grip).
4. Change one lever at a time and measure understeer gradient and limit balance (constant-radius test).
5. Check that steady and transient balance both improve; changing bars also changes transient response.

**Gotchas:** raising rear bar for rotation with power-off lift-off oversteer risk; always check stability margin at the limit.

## Verify
- [ ] Understeer gradient changes in the predicted direction and magnitude.
- [ ] Limit behaviour (power-off, brake-in-turn) still safe.
