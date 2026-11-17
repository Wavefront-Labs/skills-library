---
id: engineering-technology.chemical-engineering.piping-instrumentation.cv-calculation-liquid-and-gas
name: cv-calculation-liquid-and-gas
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-control-valve-sizing, cv-calculation-liquid-and-gas, control-valve-sizing, cv, kv, flow-coefficient, isa-75-01, iec-60534, valve-sizing, liquid-valve, gas-valve, valve-travel]
level: practitioner
status: gated
description: "Calculate control valve Cv (Kv) for liquids and gases with the IEC and ISA form, allowable pressure drop, piping factors, and the checks for travel and rangeability."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "https://www.emerson.com/documents/automation/control-valve-handbook-en-3661206.pdf (Fisher Control Valve Handbook, chapter 5)"
  - "https://fluids.readthedocs.io/fluids.control_valve.html (IEC 60534-2-1 implementation: Y = 1 - x/(3 F_gamma x_T), Kv/Cv = 1.156)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cv calculation for liquid and gas

**Goal:** the flow coefficient for a valve and the confirmation that it works across the flow range.

## Definitions
Cv is the US gpm of water at 60 F that passes with 1 psi drop; Kv is the m3/h of water at 15 C with 1 bar drop; Cv = 1.156 Kv (checked by computation: 1.1561).

## Liquids (non-choked, turbulent)
Kv = Q sqrt( (rho/rho_w) / dP ) with Q in m3/h, dP in bar, rho/rho_w the specific gravity; Cv = Q_gpm sqrt(SG/dP_psi). Apply a piping geometry factor F_p for reducers.
Viscous liquids need a Reynolds-number correction factor F_R.

## Gases and vapours (IEC 60534-2-1 form; check constants in the standard)
C = W / (N6 Fp Y sqrt(x P1 rho1)), with W the mass flow, x = dP/P1, rho1 the inlet density, N6 a units constant, and Y = 1 - x/(3 F_gamma x_T) the expansion factor; flow becomes choked when x reaches F_gamma x_T, then use x = F_gamma x_T.

## Procedure
1. Collect flows (minimum, normal, maximum), inlet pressure, outlet pressure or allowable pressure drop, temperature, fluid properties.
2. Allocate the valve dP: a rule is at least 25 to 33% of the system dynamic friction drop (or 0.7 bar, whichever larger) (gated: unconfirmed, source is paywalled or blocked).
3. Compute the required Cv at the three flows; choose a valve size so that the maximum flow is at no more than about 85 to 90% travel and the minimum at above about 10 to 20% travel; normal flow around 60 to 70% travel is a common target (gated: unconfirmed, source is paywalled or blocked).
4. Check rangeability (inherent rangeability is vendor data, often quoted 50:1 for equal percentage trim (gated: unconfirmed, source is paywalled or blocked); installed rangeability is lower).
5. Check noise (sound pressure level by the IEC 60534-8 series methods; confirm the part number for your valve type), cavitation and choked flow.
6. Confirm the actual valve's rated Cv and F_L, x_T from the vendor.

## Gotchas
- Oversizing is typical: a valve working at 10% open at normal flow controls poorly.
- Use the correct pressure drop at each flow, not the design dP for all.
- Specify the vendor and not just the size for final sizing.

## Verify
- [ ] Table of Cv required vs valve Cv at min, normal, max flow with percent travel.
- [ ] Noise and choking checks recorded.
