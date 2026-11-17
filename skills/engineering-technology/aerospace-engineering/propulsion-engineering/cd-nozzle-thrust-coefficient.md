---
id: engineering-technology.aerospace-engineering.propulsion-engineering.cd-nozzle-thrust-coefficient
name: cd-nozzle-thrust-coefficient
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, inlets, nozzles, cd-nozzle, thrust-coefficient, nozzle-expansion, over-expansion, summerfield-criterion]
level: practitioner
status: verified
description: "Size a convergent-divergent nozzle from area-Mach relations and compute thrust, thrust coefficient and over or under-expansion effects including separation."
sources:
  - "Mattingly, Elements of Propulsion"
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Anderson, Modern Compressible Flow"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Convergent-divergent nozzle and thrust coefficient

**Goal:** exit area and thrust for a given pressure ratio.

## Relations
- Choked throat: `m_dot = p_t A* sqrt(gamma/(R T_t)) (2/(gamma+1))^((gamma+1)/(2(gamma-1)))`.
- Exit Mach from the pressure ratio `p_t/p_e` (isentropic): `p_t/p_e = (1 + (gamma-1)/2 M_e^2)^(gamma/(gamma-1))`; area ratio from the area-Mach relation.
- Thrust: `F = m_dot V_e + (p_e - p_a) A_e`. Perfect expansion at `p_e = p_a`.
- Thrust coefficient (nozzle efficiency measure): `C_fg = F_actual / F_ideal`, typically 0.97-0.995 for well designed turbofan and turbojet nozzles (gated: unconfirmed, source is paywalled or blocked); includes friction, divergence and incomplete expansion losses.
- Divergence loss factor for a conical nozzle of half-angle `alpha`: `lambda = (1 + cos(alpha))/2` (0.983 at 15 degrees, computed).

## Over- and under-expansion
- Over-expanded: exit pressure below ambient; oblique shocks at the exit or flow separation inside the nozzle. Summerfield criterion (rule of thumb): separation occurs when the wall pressure falls below about 0.35-0.4 of ambient (gated: unconfirmed, source is paywalled or blocked).
- Under-expanded: lost thrust potential, expansion waves outside.

## Procedure
1. Use nozzle pressure ratio from the cycle deck over the flight envelope.
2. Choose area ratio at design point; check off-design points for over-expansion and separation.
3. Evaluate variable geometry or fixed geometry compromises.

## Verify
- [ ] The choked-flow expression was checked numerically against the area-ratio form (identical mass flow). At the design point `p_e = p_a` yields `F = m_dot V_e`.
