---
id: engineering-technology.chemical-engineering.piping-instrumentation.pump-control-and-minimum-flow
name: pump-control-and-minimum-flow
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pump-hydraulics, pump-control-and-minimum-flow, pump-control, variable-speed-drive, throttling-control, minimum-flow, recirculation-line, pump-protection, control-valve-pressure-drop, energy-saving]
level: practitioner
status: gated
description: "Choose pump flow control (control valve, VSD, recirculation), set control valve pressure drop and design minimum-flow protection against overheating."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pump control and minimum flow

**Goal:** stable flow control with acceptable energy use and pump protection.

## Control options
1. **Throttling with a control valve** on the discharge: simple, fast; wastes energy (pressure drop across the valve). A common rule is to allocate at least about 0.7 bar or 25 to 33% of the dynamic system friction drop to the valve at the design flow (gated: unconfirmed, source is paywalled or blocked), so that it has adequate authority.
2. **Variable speed drive (VSD)**: saves energy when the system has a large friction component; poor if the static head dominates (speed range narrows). Check the pump curve across the speed range, minimum speed and minimum flow.
3. **Recirculation (bypass)** of part of the flow back to suction: used for minimum flow protection and for small flow-control applications; wasteful.
4. **Parallel pumps** staged on and off for variable demand.

## Minimum flow
Operating at low flow heats the liquid (the pump efficiency loss goes into the liquid), causes recirculation inside the impeller (noise, vibration, shaft deflection), and can vaporise the liquid. Vendors give a minimum continuous stable flow (vendor data, often a stated fraction of BEP flow (gated: unconfirmed, source is paywalled or blocked)) and a minimum thermal flow. Provide a **minimum flow bypass** (orifice or control valve) to the suction vessel (not directly to the pump suction), sized to the vendor's minimum, with a flow transmitter or temperature switch for automatic control; avoid shutting the discharge valve.

## Procedure
1. Compute the system curves at minimum and maximum flow.
2. Compare energy use of throttling versus VSD over a realistic duty profile.
3. Select the control valve with sufficient pressure drop at the minimum flow.
4. Size the minimum flow line and its control or orifice; check the pump curve at that point.
5. Add protection for dry running and high discharge pressure (shutoff head).

## Gotchas
- Control valve pressure drop shrinks at high flow, making the valve lose authority.
- Bypass back to the suction line (not the vessel) raises suction temperature and NPSH issues.

## Verify
- [ ] Minimum flow bypass flow equals the vendor minimum with margin.
- [ ] Pump operating range plot for the chosen control scheme.
