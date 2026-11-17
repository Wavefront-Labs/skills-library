---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.sprayer-pump-agitation-and-tank-plumbing
name: sprayer-pump-agitation-and-tank-plumbing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, sprayer-pump-sizing, sprayer-design, agitation, centrifugal-pump, diaphragm-pump, tank-plumbing, strainer]
level: practitioner
status: draft
description: "Size a sprayer pump from application flow plus agitation and bypass, choose pump type, and lay out tank, strainers, agitation and relief plumbing."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sprayer pump, agitation and tank plumbing

**Goal:** a pump and plumbing that deliver the rate and keep the tank mixed without cavitation or pressure spikes.

## Sizing flow
`Q_pump = Q_nozzles + Q_agitation + Q_bypass + margin`

- Nozzle flow = number of nozzles x per-nozzle flow at maximum pressure and speed.
- Hydraulic agitation needs flow depending on product and tank volume; manufacturer guidance and the product label state the requirement (wettable powders and suspensions need more).
- Allow 10-20 percent margin so the pump is not at the limit and pressure remains controllable.

## Pump type
- Centrifugal: high flow, low pressure, easy to run with fine-pressure control and suited to large booms; needs priming and careful NPSH.
- Roller, diaphragm and piston: positive displacement, higher pressure (for hand-gun or high-volume use), need pressure relief, pulsation dampening and bypass.

## Plumbing
1. Suction line short, full diameter, no air leaks; strainer before the pump.
2. Pressure-side strainers and nozzle screens sized to the nozzle (finer for small nozzles).
3. Relief valve on positive displacement systems; check setting.
4. Return line, agitation jets and sparge lines positioned to avoid foam.

## Gotchas
- Foaming: use antifoam as labelled and return lines below the liquid.
- Cross-contamination: provide wash-out and tank rinse systems, as required by environmental rules.
- Chemical-compatible materials (seals, hoses).

## Verify
- [ ] At max speed and boom pressure the pump has capacity left for agitation.
- [ ] Tank holds mixing uniformity over a spraying cycle (sample and test if critical).
