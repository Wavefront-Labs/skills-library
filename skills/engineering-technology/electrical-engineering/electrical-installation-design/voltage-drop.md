---
id: engineering-technology.electrical-engineering.electrical-installation-design.voltage-drop
name: voltage-drop
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [electrical-engineering, electrical-installation-design, feeder-voltage-drop, long-feeder-voltage-drop, motor-start-voltage-drop, voltage-drop, voltage-drop-calculation]
level: practitioner
status: draft
description: "Calculate and limit voltage drop on feeders and branch circuits, including motor-starting drop and long runs."
sources:
  - "https://www.nfpa.org/"
  - "https://electrical.theiet.org/bs-7671/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Voltage drop calculation

1. **Single-phase:** `Vd = 2 I L (R cos(phi) + X sin(phi))`; **three-phase:** `Vd_LL = sqrt(3) I L (R cos(phi) + X sin(phi))`, with R and X per unit length from cable tables. For DC and small cables `X` is negligible.
2. **Percent:** `Vd% = Vd / V_nominal x 100`.
3. **Example:** 3-phase 400 V, 60 A, 80 m of cable with R = 0.727 ohm/km, X = 0.08 ohm/km, pf 0.85 (sin phi = 0.527): `Vd = 1.732 x 60 x 0.08 x (0.727 x 0.85 + 0.08 x 0.527) = 5.49 V`, 1.4 percent.
4. **Recommended limits:** NEC informational notes recommend about 3 percent on a branch circuit and 5 percent total for feeder plus branch (an advisory, not a rule); BS 7671 appendix 4 gives 3 percent lighting and 5 percent other uses from the origin for a public supply (verify the amendment in force); IEC 60364-5-52 Annex G gives similar values.
5. **Motor starting:** compute drop with starting current and low power factor (about 0.3 to 0.4); keep terminal voltage above the motor starting requirement (commonly 80 to 85 percent of rated).
6. **Long feeders:** upsize conductors or use a higher voltage; use the actual operating temperature resistance (R at 70 or 90 C is greater than R at 20 C by about 0.4 percent per kelvin).
7. Voltage drop and ampacity are separate checks; the larger conductor wins.

**Verify:** measure the voltage at the load and at the source under load and compare to the calculation.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
