---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.inverter-sizing-and-losses
name: inverter-sizing-and-losses
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [inverter-sizing, inverter, igbt, sic-mosfet, conduction-loss, switching-loss, dc-link, electric-drive]
level: practitioner
status: gated
description: "Size a traction inverter for peak phase current and DC voltage, estimate conduction and switching losses, and compare IGBT and SiC options."
sources:
  - "Mohan, Undeland and Robbins, Power Electronics"
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Inverter sizing and losses

1. Peak phase current from motor peak torque and flux (from the machine design). Rated device current must cover peak with margin and thermal limits for the peak duration.
2. DC voltage: bus must exceed motor back-EMF at maximum speed plus margin; battery voltage range at low SOC sets the real limit. 400 V and 800 V classes are common (gated: unconfirmed, source is paywalled or blocked).
3. Conduction losses: IGBT `Vce0*I + rce*I^2`; MOSFET `Rds_on*I^2`. Switching loss: `Esw*fsw` summed over devices.
4. SiC MOSFETs have lower switching and conduction losses at part load than silicon IGBTs, allowing higher fsw and better efficiency especially at light load (gated: unconfirmed, source is paywalled or blocked); cost and robustness (short-circuit capability) are considerations.
5. Thermal design: junction temperature below the datasheet limit at peak with the cooling-plate temperature; use transient thermal impedance curves for short peaks.
6. DC-link capacitor sizing for ripple current and voltage ripple; EMI filter and gate drive design affect dv/dt.
7. Functional safety: active short-circuit and discharge requirements.

**Gotchas:** datasheets are at specified temperatures; derate.

## Verify
- [ ] Peak current thermal check using transient impedance.
- [ ] Loss model compared with the supplier efficiency map.
