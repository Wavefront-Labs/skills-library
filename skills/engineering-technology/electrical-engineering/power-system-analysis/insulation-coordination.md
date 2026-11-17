---
id: engineering-technology.electrical-engineering.power-system-analysis.insulation-coordination
name: insulation-coordination
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [arrester-rating-selection, basic-impulse-level, bil, bil-and-clearance-selection, electrical-engineering, iec-60071, insulation-coordination, mcov, power-system-analysis, surge-arrester]
level: advanced
status: draft
description: "Coordinate equipment insulation with surge arresters: arrester MCOV, protective margins and BIL selection per IEC 60071 and IEEE practice."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Insulation coordination and surge protection

1. Identify representative overvoltages: continuous, temporary (earth-fault TOV, load rejection), slow-front (switching), fast-front (lightning).
2. **Arrester selection:** `MCOV` must exceed the highest continuous phase-to-ground voltage (for an effectively grounded system roughly `Um / sqrt(3)`); verify TOV capability against the earth-fault factor and duration; choose the energy class for the line discharge duty.
3. **Protective margins:** compare equipment withstand (BIL, switching impulse level) with the arrester protective level at the expected discharge current, with a margin often of at least 20 percent (check the standard in use); include separation distance because surge voltage rises along the lead.
4. **Standards route:** IEC 60071-1/-2 defines coordination withstand voltage, required withstand voltage and standard withstand voltage (apply safety and altitude factors); IEEE C62.22 guides metal-oxide arrester application (verify the number).
5. **Clearances:** air clearances follow the selected withstand level; correct for altitude above 1000 m.

**Verify:** tabulate each equipment's BIL, arrester residual voltage and the margin; revisit when a new transformer is added.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
