---
id: engineering-technology.electrical-engineering.power-system-analysis.transmission-line-modelling
name: transmission-line-modelling
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [abcd-parameters, electrical-engineering, ferranti-and-surge-impedance-loading, ferranti-effect, line-parameter-calculation, power-system-analysis, surge-impedance-loading, transmission-line, transmission-line-modelling]
level: practitioner
status: draft
description: "Model overhead lines with short, nominal-pi and long-line ABCD parameters, find surge impedance loading and the Ferranti rise."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ncees.org/engineering/pe/electrical-computer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Transmission line modelling

- **Per-phase parameters (transposed line):** inductance `L = 2e-7 ln(GMD/GMR)` H/m; capacitance `C = 2 pi e0 / ln(GMD/r_eq)` F/m. Use bundled-conductor equivalents for GMR and radius.
- **Models by length:** short (below about 80 km): `A = D = 1`, `B = Z`, `C = 0`. Medium (about 80 to 250 km), nominal pi: `A = D = 1 + YZ/2`, `B = Z`, `C = Y(1 + YZ/4)`. Long: `A = D = cosh(gamma l)`, `B = Zc sinh(gamma l)`, `C = sinh(gamma l)/Zc`, with `Zc = sqrt(z/y)`.
- **Surge impedance loading:** `SIL = V_LL^2 / Zc`. Example: 345 kV, `Zc` = 300 ohm gives 397 MW. At SIL the line neither absorbs nor produces reactive power.
- **Ferranti rise:** at no load the capacitive charging current through line inductance makes the receiving end voltage higher than the sending end; it grows with the square of length and needs shunt reactors on long lines.
- **Voltage regulation:** `(V_r,noload - V_r,fullload) / V_r,fullload`.

**Verify:** with `Zc` and `gamma l` from data, check `A D - B C = 1` for the reciprocal network.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
