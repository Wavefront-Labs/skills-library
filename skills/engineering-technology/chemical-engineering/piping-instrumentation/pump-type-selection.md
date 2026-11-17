---
id: engineering-technology.chemical-engineering.piping-instrumentation.pump-type-selection
name: pump-type-selection
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pump-hydraulics, pump-type-selection, pump-selection, centrifugal-pump, positive-displacement-pump, gear-pump, diaphragm-pump, metering-pump, pump-type, viscosity-correction]
level: practitioner
status: gated
description: "Choose between centrifugal and positive-displacement pumps (gear, screw, diaphragm, piston) from flow, head, viscosity, solids, shear and accuracy requirements."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centrifugal vs positive displacement selection

**Goal:** a pump family chosen from the duty.

## Rules of thumb
- **Centrifugal**: moderate to high flow, low to moderate head per stage, low to moderate viscosity (up to roughly 200 to 500 mPa.s with derating (gated: unconfirmed, source is paywalled or blocked)), smooth flow, simple.
- **Positive displacement (PD)**: low flow, high head, high viscosity, metering accuracy, and self-priming; flow is nearly constant against pressure, so a relief valve on the discharge is mandatory.

## Families
- **Gear and screw** pumps (rotary PD): viscous liquids, lubricity needed, shear sensitivity moderate; screws for high flow and gentle handling.
- **Diaphragm and piston/plunger** (reciprocating): very high pressure, metering, abrasive or hazardous liquids (leak-free diaphragm pumps), pulsation dampeners needed.
- **Progressing cavity**: viscous, solids-laden and shear-sensitive fluids.
- **Peristaltic, lobe**: sanitary, shear-sensitive.
- Sealless magnetic-drive and canned-motor centrifugal pumps for toxic or hazardous service (check dry-run protection and temperature limits).

## Procedure
1. List: flow range, differential pressure, viscosity at temperature, vapour pressure, solids, hazard class.
2. Screen by the flow and head regime (a specific speed or the vendor's selection chart); apply viscosity correction (Hydraulic Institute method) for centrifugal pumps on viscous liquids (gated: unconfirmed, source is paywalled or blocked).
3. For PD: check NPSHr at pump speed (lower speeds reduce NPSHr), pulsation and pipe vibration, discharge relief valve and its return.
4. Choose sealing (mechanical seal and piping plan per API 682 for refinery-type service (gated: unconfirmed, source is paywalled or blocked), or magnetic drive) and materials.
5. Compare lifecycle cost (energy, maintenance, spares).

## Gotchas
- Never deadhead a PD pump; relief valve must discharge to suction vessel or another safe location, not to the pump suction line without consideration.
- Viscous liquids lower centrifugal efficiency a lot; check before specifying.

## Verify
- [ ] Selection table with rejected alternatives and reasons.
- [ ] Relief and pulsation provisions listed for PD pumps.
