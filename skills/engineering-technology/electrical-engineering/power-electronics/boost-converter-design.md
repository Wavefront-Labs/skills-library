---
id: engineering-technology.electrical-engineering.power-electronics.boost-converter-design
name: boost-converter-design
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [boost-compensation, boost-converter, boost-converter-design, boost-inductor-peak-current, electrical-engineering, power-electronics, rhp-zero, step-up-converter]
level: practitioner
status: draft
description: "Design a boost converter: duty, inductor ripple and peak current, output capacitor, and the right-half-plane zero limiting control bandwidth."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ti.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Boost converter design

- **CCM transfer:** `Vo/Vin = 1/(1 - D)`, so `D = 1 - Vin/Vo` (ideal; losses raise D).
- **Inductor:** `L = Vin D / (dI f_sw)` with ripple `dI` about 20 to 40 percent of average input current `I_in = Io/(1 - D)`. Peak `I_pk = I_in + dI/2`; the inductor must not saturate at current limit.
- **Output capacitor:** `C >= Io D / (f_sw dVo)` for ripple from charge, plus ESR term `ESR x I_pk`.
- **Right-half-plane zero:** `f_rhp = (1 - D)^2 R / (2 pi L)`. Keep the crossover below about 1/5 to 1/3 of `f_rhp` in voltage mode; use current-mode control to simplify.
- **Diode vs synchronous rectifier:** diode reverse recovery adds loss; boost has no inherent short-circuit protection (the input source feeds the load through the diode), so add input fuse or load switch.
- **DCM:** at light load the inductor current reaches zero; the gain rises and the control loop changes.
- **Example:** 12 V to 24 V at 2 A, 200 kHz, 30 % ripple: D = 0.5, Iin = 4 A, dI = 1.2 A, `L = 12 x 0.5/(1.2 x 200k) = 25 uH`.

**Verify:** measure inductor current at maximum load and low line, and check the loop gain with a network analyser.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
