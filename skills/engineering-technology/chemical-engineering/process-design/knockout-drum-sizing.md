---
id: engineering-technology.chemical-engineering.process-design.knockout-drum-sizing
name: knockout-drum-sizing
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-equipment-sizing, knockout-drum-sizing, knockout-drum, souders-brown, vapor-liquid-separator, flash-drum, demister, k-factor, separator-sizing, vessel-sizing]
level: practitioner
status: gated
description: "Size a vertical vapour-liquid knockout drum with the Souders-Brown equation: allowable velocity, diameter, liquid hold-up height, demister and nozzle checks."
sources:
  - "Towler and Sinnott, Chemical Engineering Design; Turton et al., Analysis, Synthesis and Design of Chemical Processes; Peters, Timmerhaus and West, Plant Design and Economics (textbooks, method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vapour-liquid knockout drum sizing

**Goal:** a drum diameter and height that keeps liquid carryover at an acceptable level.

## Steps
1. **Allowable vapour velocity**: v_max = K x sqrt((rho_L - rho_V)/rho_V). K depends on orientation, demister and pressure; starting values near 0.05 to 0.11 m/s for vertical drums are common in textbooks (gated: unconfirmed, source is paywalled or blocked) (0.35 ft/s is 0.107 m/s, computed, a figure quoted for wire mesh demisters at low pressure). Reduce K at high pressure (above about 15 bar (gated: unconfirmed, source is paywalled or blocked)) and for foaming or viscous liquids; confirm with company practice or the demister vendor.
2. **Cross-section**: A = Q_V / (f x v_max), where f is a design fraction (for example 0.75 to 1) to give margin; D = sqrt(4A/pi).
3. **Liquid hold-up**: from the surge time (see `engineering-technology.chemical-engineering.process-design.surge-drum-residence-time-sizing`) and liquid rate.
4. **Height**: bottom (low-low level to tangent), hold-up between low and high level, disengagement space above high level (often at least about 0.5 to 1 m, or about 1.5 times the inlet nozzle diameter, whichever larger), and demister space; top clearance to the mesh.
5. **Nozzle sizing**: inlet momentum (rho v^2) limits (for example about 1,500 Pa to 6,000 Pa depending on the inlet device (gated: unconfirmed, source is paywalled or blocked); confirm), vapour outlet velocity, liquid outlet with vortex breaker.
6. **Check** L/D (typically 2.5 to 5 for vertical vessels (gated: unconfirmed, source is paywalled or blocked)) and the minimum diameter for the demister.

## Gotchas
- Horizontal drums need the Souders-Brown method adapted to the vapour space area.
- Entrainment from liquid slugs in two-phase lines needs an inlet device and a larger drum.
- Design for the worst case flow (maximum vapour, minimum density difference) including relief if the drum is a relief knockout.

## Verify
- [ ] Velocity at operating and maximum case below v_max.
- [ ] Height and level setpoints consistent with instrument ranges.
