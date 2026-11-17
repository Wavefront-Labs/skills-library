---
id: engineering-technology.electrical-engineering.power-electronics.converter-thermal-design
name: converter-thermal-design
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [converter-thermal-design, electrical-engineering, foster-network, heat-sink-design, junction-temperature, power-electronics, thermal-interface-materials, thermal-network-modelling, thermal-resistance]
level: practitioner
status: draft
description: "Design converter cooling: thermal resistance networks, junction temperature, heat sink sizing and interface materials."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ti.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Converter thermal design

1. **Steady state:** `Tj = Ta + P (Rth_jc + Rth_cs + Rth_sa)`; total dissipation from the loss budget at hot conditions. Example: 20 W with `Rth_jc` 0.5, `Rth_cs` 0.3, `Rth_sa` 2.0 K/W and 45 C ambient gives `Tj = 45 + 20 x 2.8 = 101 C`.
2. **Transient:** use the datasheet `Zth(t)` curve or Foster network for pulsed loads; short pulses see only the die and package.
3. **Heat sink:** natural convection roughly 5 to 10 W/m^2K; forced air improves by a factor 3 to 10; allow for altitude and filter clogging. Check the available vendor Rth versus flow.
4. **Interface:** thermal pad or grease (thermal conductivity a few W/mK) with correct mounting pressure; isolation pads add resistance.
5. **Derating:** keep Tj at least 20 to 25 C below the maximum for reliability; capacitors halve in life for each 10 C rise (electrolytics).
6. **Spreading and PCB copper:** more copper area and thermal vias reduce Rth for SMD packages.
7. Confirm by thermocouple or infrared camera and compensate for measurement error.

**Verify:** run at the highest ambient and load until steady state and compare the measured case temperature with the model.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
