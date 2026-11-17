---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.spray-dryer-design-and-operation
name: spray-dryer-design-and-operation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, spray-drying, food-drying, dehydration, atomizer, rotary-atomizer, cyclone, powder, dust-explosion, milk-powder]
level: practitioner
status: draft
description: "Specify a spray dryer: atomiser type, inlet and outlet temperature, chamber size from droplet drying time, powder separation, product properties and dust explosion safeguards."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Earle, Unit Operations in Food Processing"
  - "Fellows, Food Processing Technology: Principles and Practice"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Spray dryer design and operation

**Goal:** a powder of target moisture, particle size and bulk density at an acceptable energy cost.

## Elements
- **Atomisers**: rotary wheel (wide chamber, broader size range, handles abrasive feed), pressure nozzle (narrow spray, coarser, taller chamber), two-fluid nozzle (fine droplets, small-scale).
- **Air**: heated to roughly 150-250 C at the inlet; outlet typically about 70-100 C. The outlet temperature is controlled by feed rate; it sets final moisture. Evaporative cooling keeps product temperature far below inlet air temperature during constant-rate drying.
- **Chamber**: sized for the time for the largest droplets to dry before touching walls; co-current flow protects heat-sensitive products.
- **Separation**: cyclones plus bag filters or wet scrubbers; fines return can agglomerate powder.

## Design checks
1. Heat and mass balance: air flow from the psychrometric balance, feed solids content (higher solids reduce evaporation load but raise viscosity).
2. Droplet-size and chamber-diameter estimates from pilot trials; vendors often scale from pilot data.
3. Powder properties: Tg of amorphous powders (stickiness), carrier addition (maltodextrin) for sugar-rich products.
4. Energy recovery from exhaust, and multi-stage drying with fluid bed after-dryer for better efficiency and agglomerates.

## Safety
Combustible food powders form explosive dust clouds. Follow fire and dust explosion standards such as NFPA 61 (agricultural and food processing) and NFPA 652, or ATEX in the EU: housekeeping, explosion venting or suppression, grounding, hot-spot control, and a documented dust hazard analysis.

## Verify
- [ ] Outlet air temperature and powder moisture correlate on trial.
- [ ] Dust hazard analysis complete and protection devices maintained.
