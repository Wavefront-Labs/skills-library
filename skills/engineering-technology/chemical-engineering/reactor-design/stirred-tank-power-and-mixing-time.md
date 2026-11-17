---
id: engineering-technology.chemical-engineering.reactor-design.stirred-tank-power-and-mixing-time
name: stirred-tank-power-and-mixing-time
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-scale-up-and-mixing, stirred-tank-power-and-mixing-time, stirred-tank, power-number, mixing-time, agitation]
level: practitioner
status: verified
description: "Calculate agitator power, pumping capacity and mixing time for a baffled stirred tank with the power number."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stirred tank power and mixing time

**Goal:** Calculate agitator power, pumping capacity and mixing time for a baffled stirred tank with the power number.

## Steps
1. Power P = Np rho N^3 D^5 in the turbulent regime (Re above roughly 10,000 (gated: unconfirmed, source is paywalled or blocked)), where Np is the power number of the impeller (about 5 for a Rushton turbine, about 1.3 for a four-blade 45 degree pitched-blade turbine, about 0.3 for some hydrofoils such as the A310 (secondary tabulations only (gated: unconfirmed, source is paywalled or blocked); Np varies with blade count and geometry); confirm with vendor data).
2. Reynolds number Re = rho N D^2 / mu; in laminar flow P is proportional to mu N^2 D^3.
3. Mixing time in turbulent flow is roughly constant times 1/N for a given geometry; correlations give N times t_mix of the order tens for typical impellers (gated: unconfirmed, source is paywalled or blocked).
4. Check that gassing reduces the power draw and add that effect for gas-liquid duty.
5. Select the motor with a margin on shaft power and gearbox efficiency.

## Gotchas
- Unbaffled tanks vortex and change Np.
- Impeller type and clearance affect all values; use manufacturer data for final design.

## Verify
- [ ] Power per volume lies in the usual range for the duty.
- [ ] Mixing time meets the process requirement.
