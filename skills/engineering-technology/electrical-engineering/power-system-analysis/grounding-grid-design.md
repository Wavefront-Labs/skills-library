---
id: engineering-technology.electrical-engineering.power-system-analysis.grounding-grid-design
name: grounding-grid-design
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [electrical-engineering, gpr, ground-grid, ground-potential-rise, grounding-grid-design, ieee-80, power-system-analysis, soil-resistivity-interpretation, step-and-touch-voltage, substation-grounding]
level: advanced
status: draft
description: "Design a substation grounding grid to IEEE 80: tolerable step and touch voltages, grid resistance, GPR and mesh voltage checks."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Substation grounding grid design (IEEE Std 80)

1. **Soil:** measure resistivity (Wenner four-pin) at several spacings and fit a two-layer model; do not use a single reading.
2. **Tolerable voltages (70 kg body, fault duration `ts`):** `Etouch70 = (1000 + 1.5 Cs rho_s) 0.157 / sqrt(ts)`, `Estep70 = (1000 + 6 Cs rho_s) 0.157 / sqrt(ts)`; the 50 kg coefficient is 0.116. `Cs` corrects for a surface layer of resistivity `rho_s` and thickness `hs`.
3. **Grid resistance (Sverak):** `Rg = rho [1/LT + 1/sqrt(20 A) (1 + 1/(1 + h sqrt(20/A)))]` with buried conductor length `LT`, area `A`, depth `h`.
4. **GPR:** `GPR = Ig Rg`, with `Ig` the symmetrical grid current after the split factor (current returning via shield wires and neutrals) and decrement factor.
5. **Mesh and step voltages:** `Em = rho Km Ki Ig / LM`, `Es = rho Ks Ki Ig / LS`; they must stay below the tolerable values; if not, tighten spacing, add rods at the perimeter, extend surface layer.
6. Check transferred potential to fences, pipelines and communications.

**Verify:** after construction, measure grid resistance by fall-of-potential and verify bonding continuity between equipment and grid.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
