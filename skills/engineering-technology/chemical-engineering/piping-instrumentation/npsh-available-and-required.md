---
id: engineering-technology.chemical-engineering.piping-instrumentation.npsh-available-and-required
name: npsh-available-and-required
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pump-hydraulics, npsh-available-and-required, npsh, npsha, npshr, cavitation, suction-pressure, vapor-pressure, pump-suction, net-positive-suction-head]
level: practitioner
status: gated
description: "Calculate NPSH available from suction conditions, compare with the pump NPSH required, apply margins, and fix cavitation risks by changing levels, line size or fluid temperature."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPSH available and required

**Goal:** avoid cavitation by showing NPSH available exceeds NPSH required with margin at all operating cases.

## NPSH available
NPSHa = (P_s - P_v)/(rho g) + z_s - h_f,s (+ velocity head term, usually neglected at the source vessel)
where P_s is the absolute pressure at the liquid surface in the suction vessel, P_v the vapour pressure at the pumping temperature, z_s the static height of liquid surface above the pump centreline (negative for suction lift), h_f,s the friction head loss in the suction line and fittings.

## NPSH required
From the pump vendor curve (NPSH3, the value at 3% head drop). The pump needs NPSHa greater than NPSHr plus a margin; common practice is a margin of about 0.5 to 1 m or a ratio of 1.1 to 1.3 (gated: unconfirmed, source is paywalled or blocked), larger for high-energy or critical pumps; follow the company standard and ANSI/HI 9.6.1. NPSHr rises with flow, so evaluate at the maximum flow.

## Worst case for NPSHa
Minimum liquid level, maximum temperature (highest vapour pressure), lowest vessel pressure, fouled strainer, maximum flow. For boiling liquids from a column or drum, P_s = P_v, so NPSHa = z_s - h_f,s: elevation is all you have.

## Fixes
Raise the vessel (or lower the pump), enlarge the suction line, reduce fittings, cool the liquid, increase vessel pressure, or choose a pump with lower NPSHr (larger eye, lower speed, inducer, or a vertical can pump).

## Worked example
Water at 60 C (vapour pressure 0.1995 bar absolute, IAPWS via CoolProp), open tank at 1.013 bar, surface 2 m above the pump centreline, suction line loss 0.5 m: NPSHa = (1.013e5 - 0.2e5)/(983 x 9.81) + 2 - 0.5 = 8.43 + 1.5 = 9.9 m (water density at 60 C 983.2 kg/m3, IAPWS via CoolProp; recomputed 9.93 m).

## Gotchas
- Data sheet NPSHa should state the basis (minimum level and so on).
- NPSH3 is not a no-damage limit for long-life operation.

## Verify
- [ ] NPSHa versus flow curve plotted against NPSHr for the maximum flow and worst case.
- [ ] Margin meets the project standard.
