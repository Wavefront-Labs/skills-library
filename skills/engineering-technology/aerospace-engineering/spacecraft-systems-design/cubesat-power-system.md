---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.cubesat-power-system
name: cubesat-power-system
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [cubesat-power, cubesat-eps, solar-cells, mppt, power-budget, smallsat-cubesat]
level: practitioner
status: verified
description: "Size a CubeSat power system: body-mounted or deployable arrays, orbit-average power, MPPT, battery and the CDS inhibit and protection requirements."
sources:
  - "CubeSat Design Specification (Cal Poly)"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "CubeSat Design Specification Rev 14.1 (February 2022): https://www.nasa.gov/wp-content/uploads/2018/01/cubesatdesignspecificationrev14_12022-02-09.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# CubeSat power

**Goal:** orbit-average power that supports the payload, communications and attitude control.

## Power generation
- Triple-junction cells have efficiency near 28 to 30 percent (gated: unconfirmed, source is paywalled or blocked) (check the datasheet at the operating temperature and end of life).
- Power from a fully illuminated face: `P = eta * S * A * f_pack * cos(theta)`, with solar constant `S` about 1361 W/m^2. Example: one 3U long face (0.1 m x 0.3 m = 0.03 m^2) at 29 percent efficiency and 0.8 packing gives 9.5 W at normal incidence (computed).
- Orbit average is much lower: tumbling or body-mounted arrays see a fraction of this; deployable panels raise it substantially.

## Electrical power system
1. Maximum power point tracking converters per array string; or direct energy transfer.
2. Li-ion or Li-polymer cells (for example commercial cylindrical cells) with protection circuits; vacuum rating and venting.
3. Regulators for 3.3 V, 5 V and the unregulated battery bus.
4. Power distribution with switches, current limits and under-voltage lockout.
5. Budget with margin: generation (orbit average with eclipse) versus loads by mode (see eclipse-power-and-battery-sizing and power-and-mass-budgets).

## CDS compliance items (check the current revision)
- Deployment switch (at least one) and a remove-before-flight pin (CDS Rev 14.1 sections 2.3.2 and 2.3.5): the satellite must be fully off during launch until deployed.
- Battery safety: protection against over-charge, over-discharge and short circuit; launch providers review battery design and tests.
- Inhibits against inadvertent activation of deployables and transmitters.

## Gotchas
- Fully charged batteries at launch need handling; a charging plan on the pad is limited.
- Safe-mode power must sustain the satellite in the worst attitude after tumbling.
- Cell temperature affects charging limits for Li-ion (no charging below around 0 degrees Celsius (gated: unconfirmed, source is paywalled or blocked), check datasheet).

## Verify
- [ ] The power budget by mode shows non-negative battery energy balance per orbit including the worst-case attitude and eclipse.
