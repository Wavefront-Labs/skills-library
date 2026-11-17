---
id: engineering-technology.chemical-engineering.piping-instrumentation.choked-flow-cavitation-flashing
name: choked-flow-cavitation-flashing
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-control-valve-sizing, choked-flow-cavitation-flashing, choked-flow, cavitation, flashing, fl-factor, ff-factor, valve-noise, anti-cavitation-trim, pressure-recovery, liquid-pressure-recovery]
level: advanced
status: gated
description: "Check control valves for choked flow, cavitation and flashing with FL and FF, incipient cavitation indices and mitigation by trim selection or staged pressure drop."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "https://www.emerson.com/documents/automation/control-valve-handbook-en-3661206.pdf (Fisher Control Valve Handbook, chapter 5: F_F, choked dP is the lesser of actual and choked)"
  - "https://fluids.readthedocs.io/fluids.control_valve.html (open-source IEC 60534-2-1 implementation: F_F = 0.96 - 0.28 sqrt(Pv/Pc))"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choked flow, cavitation and flashing

**Goal:** avoid valve damage, noise and loss of capacity.

## Liquid choked flow
Maximum pressure drop before choking: dP_choked = F_L^2 (P1 - F_F P_v), with F_L the liquid pressure recovery factor (vendor data; it depends on valve style and trim, so take F_L from the vendor, not a rule of thumb), P_v the vapour pressure and F_F = 0.96 - 0.28 sqrt(P_v/P_c) the critical-pressure ratio factor. If the actual dP exceeds this, flow is choked and Cv is calculated with dP_choked.

## Cavitation vs flashing
- **Cavitation**: the local pressure at the vena contracta falls below P_v, vapour forms, and then the downstream pressure recovers above P_v so the bubbles collapse and damage metal (noise, vibration, pitting). Occurs when the downstream pressure is above vapour pressure but dP is large.
- **Flashing**: downstream pressure is below the vapour pressure; the vapour stays; erosion and high velocity two-phase flow; size the downstream piping as two-phase; hardened materials and angle bodies help.
- **Incipient cavitation index** (K_c or sigma): cavitation starts at dP below the choked value, about K_c (P1 - P_v) with K_c from vendor data (gated: unconfirmed, source is paywalled or blocked); damaging cavitation begins above a higher dP.

## Mitigation
1. Reduce the pressure drop across one valve by staging (two valves in series) or using multi-stage trim.
2. Use anti-cavitation or multi-stage trim, hardened materials, or install the valve where the downstream pressure is higher (for example at the end of a line).
3. Flashing: use angle or axial-flow valves, larger body size downstream, hardened trim and short outlet piping.
4. For noise, use low-noise trim and thicker pipe downstream.

## Gotchas
- Check at all operating points, especially the minimum flow where the valve dP is largest.
- Vapour pressure from the maximum temperature case.

## Verify
- [ ] Table of dP, dP_choked and the incipient cavitation limit at each flow case.
- [ ] Vendor trim confirmed for the severe case.
