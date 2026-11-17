---
id: engineering-technology.chemical-engineering.reactor-design.multiple-steady-states-in-cstr
name: multiple-steady-states-in-cstr
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-heat-effects-and-stability, multiple-steady-states-in-cstr, multiple-steady-states, cstr-stability, heat-generation-curve, heat-removal-line, ignition-extinction, hysteresis, exothermic-cstr, van-heerden]
level: advanced
status: draft
description: "Find multiple steady states and stability of an exothermic CSTR using heat-generation and heat-removal curves, ignition and extinction points, and control implications."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiple steady states and stability of a CSTR

**Goal:** know whether an exothermic CSTR can sit on more than one steady state and which are stable.

## Van Heerden analysis
- **Heat removal** R(T) = F rho c_p (T - T0) + U A (T - T_c): a straight line in T (slope = F rho c_p + U A).
- **Heat generation** G(T) = (-Delta H_r) F_A0 X(T), where X(T) comes from the mole balance with rate k(T): an S-shaped curve for first-order exothermic reactions.
- Steady states are the intersections of G and R.

## Stability
A steady state is stable if the slope of R exceeds the slope of G at the intersection (dR/dT > dG/dT). The middle of three intersections is unstable (it is the one that is never observed); lower is the low-conversion state, upper is the high-conversion state.

## Ignition and extinction
Increasing feed temperature moves the line; at the ignition point the low state vanishes and the reactor jumps to the upper state; reversing, it jumps down at the extinction point at a lower temperature (hysteresis).

## Procedure
1. Compute G(T) and R(T) in a spreadsheet for a range of T.
2. Mark intersections; classify stability.
3. Vary residence time, feed temperature and coolant temperature to map the region of multiplicity.
4. Pick a design point away from ignition or extinction, with margin.
5. Verify control: a temperature loop that cools by manipulating coolant must keep the unit on the stable branch; analyse dynamic stability with the linearised model.

## Gotchas
- Stable steady states can still be dynamically unstable (oscillatory) for some parameter sets.
- Start-up path must reach the upper state without overshoot.

## Verify
- [ ] Intersections and slopes computed and plotted.
- [ ] Margin from ignition and extinction points stated.
