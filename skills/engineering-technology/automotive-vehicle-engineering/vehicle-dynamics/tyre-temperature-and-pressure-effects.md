---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.tyre-temperature-and-pressure-effects
name: tyre-temperature-and-pressure-effects
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [tyre-thermal, tyre-pressure, tyre-temperature, hot-pressure, cold-pressure, gas-law, tyre-behaviour]
level: practitioner
status: gated
description: "Predict hot tyre pressure from cold pressure with the gas law, and know how pressure and temperature change stiffness, grip and rolling resistance."
sources:
  - "Pacejka, Tire and Vehicle Dynamics"
  - "tyre manufacturer technical manuals"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tyre temperature and pressure effects

- **Gas law (absolute units):** `P_hot = P_cold*T_hot/T_cold` using gauge+atmospheric pressure converted to absolute and temperatures in kelvin. Example: 220 kPa gauge (321 kPa abs) at 20 C (293 K) heated to 50 C (323 K) gives 354 kPa abs, about 253 kPa gauge. Real tyres gain slightly different amounts as the volume changes; log measured values. (Gas-law example recomputed: 321.3 kPa abs x 323/293 = 354.2 kPa abs = 252.9 kPa gauge.)
- Pressure sets vertical stiffness, cornering stiffness (rises with pressure), contact patch size and rolling resistance (falls as pressure rises). Too high a pressure lowers grip on rough surfaces and increases wear in the centre.
- Temperature: grip rises as the tread warms into its optimum window, then falls when it overheats; this window depends on compound.
- Test practice: set **cold** pressure with the tyre sitting for hours out of the sun; record ambient; measure hot pressure straight after the run; plan cold-set targets to hit a hot target.
- Use the vehicle placard/manufacturer cold pressure as the baseline for road cars.

**Gotchas:** altitude and nitrogen vs air make little difference compared with temperature (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Predicted hot pressure within a few kPa of measured.
- [ ] Documented cold-set target and ambient for each run.
