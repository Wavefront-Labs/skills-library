---
id: engineering-technology.chemical-engineering.piping-instrumentation.liquid-line-sizing
name: liquid-line-sizing
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-line-sizing, liquid-line-sizing, line-sizing, liquid-lines, pipe-velocity, pressure-drop, pump-suction-line, pump-discharge-line, economic-pipe-diameter, pipe-diameter]
level: practitioner
status: gated
description: "Size liquid process lines from velocity and pressure-drop criteria, with suction versus discharge limits, erosion and noise checks, and a worked pipe selection."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Liquid line sizing

**Goal:** a nominal pipe size that meets pressure drop, velocity and economic criteria.

## Criteria (indicative; follow your company standard)
- **Pump suction**: low velocity to protect NPSH, roughly 0.5 to 1.5 m/s and a low pressure-drop limit (a few kPa per 100 m is common).
- **Pump discharge and general process liquids**: about 1 to 3 m/s, and a pressure drop typically 0.2 to 1 bar per 100 m depending on the service (gated: unconfirmed, source is paywalled or blocked).
- **Gravity flow and drain lines**: sized for partially full flow, with slope.
- Viscous liquids: size on pressure drop, since velocity is low.
- Erosion limits for solids-laden or corrosive liquids: lower velocities, a maximum of about 1 to 2 m/s for slurries (varies (gated: unconfirmed, source is paywalled or blocked)).
- Water hammer: limit velocity on lines with fast-closing valves.

## Procedure
1. Compute volumetric flow Q at the design case (design margin included).
2. Choose a trial inner diameter from the velocity target: D = sqrt(4 Q/(pi v)); pick the nearest NPS and schedule (inner diameter from the schedule table).
3. Compute actual velocity, Reynolds number and friction pressure drop with the Darcy equation: dP = f (L/D) rho v^2/2 (see the Colebrook skill), plus fittings (K method) and static head.
4. Check against the pressure-drop limit; step up the size if over.
5. Compare the economic optimum: larger pipe costs more but saves pumping energy; an economic diameter for turbulent flow in carbon steel is often near D (m) about 0.363 q^0.45 rho^0.13 with q the VOLUMETRIC flow in m3/s and rho in kg/m3 (Peters and Timmerhaus form (gated: unconfirmed, source is paywalled or blocked); their US-unit form 3.9 Q^0.45 rho^0.13 converts to a coefficient of 0.343, so treat it as a +-10% screening value; for 40 m3/h water it gives about 0.12 m). Do not insert mass flow.
6. Document in a line list: line number, fluid, flow, size, velocity, dP per 100 m.

## Worked example
Water at 40 m3/h (0.0111 m3/s) in 80 mm NPS Sch 40 (inner diameter 77.9 mm): v = 0.0111/(pi/4 x 0.0779^2) = 2.33 m/s; Re about 1.8e5; f about 0.02 (Colebrook gives 0.0194 at Re 1.8e5, 0.68 bar); dP per 100 m = 0.02 x (100/0.0779) x 1000 x 2.33^2/2 = 0.70 bar. Acceptable for discharge; too high for suction.

## Gotchas
- Pressure drop at maximum flow, not at normal.
- Check flashing risk near saturated liquids at the downstream end.

## Verify
- [ ] Velocity and dP per 100 m within criteria.
- [ ] Line list and calculation sheet reference the same flow case.
