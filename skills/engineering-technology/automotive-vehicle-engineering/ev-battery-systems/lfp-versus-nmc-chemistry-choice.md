---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.lfp-versus-nmc-chemistry-choice
name: lfp-versus-nmc-chemistry-choice
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [lfp-vs-nmc, lfp, nmc, nca, cathode-chemistry, lithium-iron-phosphate, chemistry-selection]
level: practitioner
status: gated
description: "Choose between LFP and nickel-rich (NMC/NCA) cathodes on energy density, cost, cycle life, safety, cold performance, SOC estimation and supply chain."
sources:
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
  - "Linden and Reddy, Handbook of Batteries"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# LFP versus NMC chemistry choice

| Aspect | LFP | NMC/NCA |
|---|---|---|
| Energy density | Lower (cell level, Wikipedia LFP page lists 95-172 Wh/kg specific energy and 180-205 Wh/kg next-gen (CATL announcement it cites)) | Higher (roughly 220-300 Wh/kg class (gated: unconfirmed, source is paywalled or blocked)); check supplier data |
| Cost | Lower, no nickel/cobalt | Higher, price depends on metals |
| Cycle life | Typically very high | Good, depends on formulation and operation |
| Thermal stability | Better (higher runaway onset, less oxygen release (gated: unconfirmed, source is paywalled or blocked)) | Lower margin, needs strong propagation design |
| Voltage | Flat (3.2 V nominal, Wikipedia LFP battery), flat OCV curve makes SOC estimation harder, hysteresis | Sloped OCV, easier SOC |
| Cold | Power drops more at low temperature | Better, though still limited |
| Notes | Often charged to 100% routinely; calibration SOC reset needed | Avoid long time at high SOC |

- Choose by vehicle role: standard-range, cost-driven, high-cycle (fleet) -> LFP; long range, performance, packaging limited -> NMC.
- Figures change quickly; use current supplier datasheets and independent test data.
- Consider mixed packs or a chemistry per variant using the same platform.

**Gotchas:** flat OCV demands better current integration, periodic full-charge calibration.

## Verify
- [ ] Decision matrix completed with datasheet values and weights.
- [ ] BMS algorithm plan addresses the chosen chemistry's SOC behaviour.
