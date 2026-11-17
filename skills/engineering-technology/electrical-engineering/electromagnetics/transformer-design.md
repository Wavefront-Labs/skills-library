---
id: engineering-technology.electrical-engineering.electromagnetics.transformer-design
name: transformer-design
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [electrical-engineering, electromagnetics, iec-60076, open-short-circuit-tests, transformer-design, transformer-equivalent-circuit, transformer-inrush, transformer-regulation, turns-ratio]
level: practitioner
status: draft
description: "Design and test power transformers: turns ratio, equivalent circuit parameters from open and short-circuit tests, regulation and inrush."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Transformer design and testing

1. **EMF equation:** `E = 4.44 f N Phi_max = 4.44 f N Bmax Ae`; choose `Bmax` below saturation (about 1.5 to 1.7 T for grain-oriented steel, lower with margin for overvoltage).
2. **Equivalent circuit parameters:** open-circuit test (rated voltage on LV, HV open) gives core loss `Pc` and magnetising current: `Rc = V^2/Pc`; short-circuit test (rated current with a low voltage) gives copper loss `Pcu` and `Zsc = Vsc/Irated`.
3. **Regulation:** `VR ~ (I R cos(phi) +/- I X sin(phi))` per unit (plus for lagging); efficiency maximum when copper loss equals core loss.
4. **Example:** 100 kVA, 2 percent resistance, 4 percent reactance at 0.8 lagging load: `VR ~ 0.02 x 0.8 + 0.04 x 0.6 = 4.0 %`.
5. **Inrush:** energisation at voltage zero with residual flux gives peak current 5 to 10 times rated (richer in 2nd harmonic) lasting seconds; control with point-on-wave closing or pre-insertion resistors.
6. **Standards:** IEC 60076 series (power transformers) and IEEE C57 series; dielectric tests, temperature rise, and short-circuit withstand are type or special tests.
7. Cooling classes (ONAN, ONAF, ODAF) set rating.

**Verify:** compare test-derived impedance with the nameplate and with the value used in the short-circuit study.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
