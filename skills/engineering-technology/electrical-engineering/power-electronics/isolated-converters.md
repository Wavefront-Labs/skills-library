---
id: engineering-technology.electrical-engineering.power-electronics.isolated-converters
name: isolated-converters
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [electrical-engineering, flyback-converter, flyback-transformer-design, forward-converter, isolated-converters, isolated-dc-dc, llc-resonant-converter, power-electronics, smps]
level: advanced
status: draft
description: "Design flyback, forward and LLC isolated converters: turns ratio, magnetising inductance, reset and resonant tank selection."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ti.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Isolated converter topologies

**Flyback (to about 100 W):** the transformer stores energy. Choose the reflected voltage `Vor = n (Vo + Vf)` (typically 80 to 120 V), duty `D = Vor/(Vor + Vin_min)`, primary inductance `Lp = (Vin_min D)^2 / (2 Pin f_sw)` for boundary conduction (DCM/QR), peak current `Ipk = 2 Pin/(Vin_min D)`. Include the leakage inductance clamp (RCD or active clamp) and the drain voltage `Vin_max + Vor + spike`.
**Forward (100 to 500 W):** the transformer passes energy during on time; the output inductor smooths; needs a reset winding or active clamp (D below 0.5 for simple reset). `Vo = Vin D / n`.
**LLC resonant (high efficiency, 100 W to kW):** gain is controlled by frequency around the resonance `fr = 1/(2 pi sqrt(Lr Cr))`; choose `Ln = Lm/Lr` (typically 4 to 8) and `Q` from the load; aim for zero-voltage switching of the primary and zero-current switching of the rectifier; use first harmonic approximation for design and a time-domain simulation to verify.
**Common:** isolation barrier ratings (creepage and clearance per IEC 62368-1 or IEC 60664-1), feedback via optocoupler or isolated amplifier, and transformer safety insulation.

**Verify:** check the peak drain voltage, core flux density (stay below about 0.25 T ferrite) and thermal rise at full load.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
