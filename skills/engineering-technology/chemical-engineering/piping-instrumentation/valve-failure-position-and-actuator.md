---
id: engineering-technology.chemical-engineering.piping-instrumentation.valve-failure-position-and-actuator
name: valve-failure-position-and-actuator
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-control-valve-sizing, valve-failure-position-and-actuator, fail-safe-position, fail-open, fail-closed, valve-actuator, spring-and-diaphragm, positioner, air-to-open, valve-thrust, shutdown-valve]
level: practitioner
status: gated
description: "Select control valve fail position and actuator (spring-diaphragm, piston) from the hazard review, plus actuator thrust and positioner basics."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "https://www.emerson.com/documents/automation/control-valve-handbook-en-3661206.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Valve failure position and actuator selection

**Goal:** the safe action on loss of air or signal, and an actuator that can stroke the valve against process forces.

## Fail position
Decide **fail open (FO)**, **fail closed (FC)** or **fail in last position (often abbreviated FL; confirm against the project legend)** (gated: unconfirmed, source is paywalled or blocked) from the consequence of loss of the instrument air or signal:
- Cooling water to an exothermic reactor jacket: fail open.
- Steam or fuel to a heater or reboiler, reactant feed to a reactor: fail closed.
- Reflux or minimum flow lines: usually fail open.
- Pressure relief to flare or vent: fail open.
Document the decision in the hazard review (see the HAZOP skills) and on the P&ID.

## Actuators
- **Spring-and-diaphragm** pneumatic: common and reliable; the spring sets fail position (air-to-open means fail-closed; air-to-close means fail-open).
- **Piston** actuators for higher thrust or higher air pressures; use a spring-return type for fail action, or a volume tank for double-acting types ("fail in last position" or "fail to a position with a reservoir").
- **Electric and hydraulic** actuators where air is unavailable.

## Sizing
1. Required thrust or torque = seating load (to meet the shutoff class) + friction (packing) + unbalance force from the pressure acting on the plug (depends on flow direction and trim).
2. Select an actuator with a safety factor; the minimum supply pressure must be adequate (for example a 4 to 5 barg (gated: unconfirmed, source is paywalled or blocked) instrument air minimum) at the lowest air pressure.
3. Add a **positioner** for modulating service (to overcome friction and hysteresis); consider volume boosters for speed; manual handwheel or bypass if allowed by the plant philosophy.

## Gotchas
- Valve action (air-to-open vs air-to-close) reverses the controller action; document as direct or reverse acting.
- Shutdown (emergency) valves need partial stroke testing and defined closure times; they belong to the safety instrumented function (see the SIL skills) and require qualified design.

## Verify
- [ ] Fail position entry in the P&ID valve list with the reason.
- [ ] Actuator thrust margin and minimum air supply pressure stated.
