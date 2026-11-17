---
id: engineering-technology.electrical-engineering.power-electronics.magnetics-design
name: magnetics-design
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [area-product, core-loss-estimation, electrical-engineering, ferrite, inductor-design, litz-wire, magnetics-design, power-electronics, steinmetz, winding-loss-and-litz]
level: advanced
status: draft
description: "Design converter inductors and transformers with the area-product method: core loss, winding loss, fringing and litz wire."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Magnetics design for converters

1. **Specify:** inductance `L`, peak current `Ipk`, RMS current, frequency, ripple, temperature rise.
2. **Area product:** `Ap = Ae Aw >= L Ipk Irms / (Bmax J ku)` (J current density about 3 to 5 A/mm^2 natural cooling, ku fill factor about 0.3 to 0.4 for round wire); choose a core with larger Ap.
3. **Turns and gap:** `N = L Ipk/(Bmax Ae)`; gap `lg = mu0 N^2 Ae / L` (neglecting core reluctance); include fringing which raises effective inductance, so confirm with an FEA or the vendor tool.
4. **Core loss:** Steinmetz `Pv = k f^a B^b` with ripple flux amplitude (not the DC bias); use vendor data and the improved generalised Steinmetz for non-sinusoidal flux.
5. **Winding loss:** skin depth `delta = sqrt(rho/(pi f mu0))` (about 0.2 mm in copper at 100 kHz) and proximity effect; use litz or foil and interleave windings.
6. **Thermal:** total loss over surface area; rise estimate `dT = P/(h A)` with h ~ 10 W/m^2/K natural convection.
7. **Saturation margin** at the worst temperature (ferrite Bsat falls near 100 C, about 0.3 to 0.4 T for power ferrite).

**Verify:** measure inductance versus DC bias and the temperature rise in a bench test.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
