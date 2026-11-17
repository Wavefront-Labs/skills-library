---
id: engineering-technology.electrical-engineering.protection-coordination.differential-protection
name: differential-protection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [87b, 87t, busbar-protection, differential-protection, electrical-engineering, inrush-harmonic-restraint, protection-coordination, slope-characteristic-setting, transformer-differential]
level: advanced
status: draft
description: "Set transformer and busbar differential relays: slope characteristic, inrush and overexcitation restraint, CT matching."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Transformer and bus differential protection

1. **Operating characteristic:** operate current `Idiff = |I1 + I2|` against restraint `Irest`; a dual-slope curve with minimum pickup (typically 0.2 to 0.3 pu of rating), slope 1 (about 25 to 40 percent) and slope 2 (about 60 to 80 percent) at high currents. Follow the relay manual.
2. **Transformer connections:** compensate vector group phase shift and ratio (digital relays do it in software; electromechanical used delta-connected CTs). Remove zero-sequence on grounded-wye windings.
3. **Inrush restraint:** block or restrain on the 2nd harmonic content (commonly 15 to 20 percent) and cross-block between phases; **overexcitation** on 5th harmonic.
4. **Tap changer range:** include the tap range in the slope so the unit does not trip for an out-of-range tap.
5. **Busbar differential:** high-impedance (stabilising resistor sized from the maximum through-fault voltage across the CT secondary) or low-impedance numerical with CT saturation detection. Matched CTs required for high-impedance schemes.
6. **CT saturation** during external faults is the main misoperation cause.

**Verify:** energise the transformer under supervision and record inrush behaviour; perform primary injection or secondary stability checks.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
