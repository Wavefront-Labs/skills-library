---
id: engineering-technology.electrical-engineering.electromagnetics.eddy-currents-and-skin-effect
name: eddy-currents-and-skin-effect
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [busbar-proximity-effect, eddy-current-loss, eddy-currents-and-skin-effect, electrical-engineering, electromagnetics, lamination-design, proximity-effect, skin-depth, skin-effect]
level: advanced
status: draft
description: "Quantify eddy-current loss, skin and proximity effect in laminations, busbars and conductors."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Eddy currents and skin effect

- **Skin depth:** `delta = sqrt(2 rho / (w mu)) = sqrt(rho/(pi f mu))`. Copper (rho = 1.68e-8 ohm m): 9.3 mm at 50 Hz, 8.5 mm at 60 Hz, 0.066 mm at 1 MHz. Aluminium at 50 Hz about 11.8 mm.
- **AC resistance:** conductors thicker than about 2 delta show `R_ac/R_dc` rising; for large busbars use the manufacturer's data or finite element analysis; flat busbar arrangement and phase interleaving reduce proximity effect.
- **Eddy loss in laminations:** `P_e = k_e f^2 B^2 t^2` per unit volume; reduce by thinner laminations (0.23 to 0.35 mm for grain-oriented steel at 50/60 Hz), higher resistivity (silicon content), and insulation coatings.
- **Stray losses:** leakage flux in tank walls and clamps raises hot-spot temperature; use shunts or non-magnetic steel near high-current leads.
- **Conductor choice at high frequency:** litz wire with strands under delta, or foil winding thickness near one skin depth for the lowest loss in transformers.
- **Ampacity effect:** cables in trefoil vs flat formation and armoured cables have additional sheath and armour eddy losses; use the IEC 60287 method.

**Verify:** measure AC resistance at the operating frequency with an LCR meter or loss measurement and compare with the model.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
