---
id: engineering-technology.electrical-engineering.power-electronics.switch-selection
name: switch-selection
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [electrical-engineering, gan, igbt, mosfet-selection, parallel-device-current-sharing, power-device, power-electronics, sic-mosfet, switch-selection, switching-loss-estimation]
level: practitioner
status: draft
description: "Select MOSFET, IGBT and SiC devices: voltage and current margins, conduction and switching loss, and paralleling."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ti.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Power switch selection

1. **Voltage:** rating at least 1.2 to 1.5 times the maximum bus plus overshoot (derate from the datasheet's maximum, for example 1200 V device on a 600 to 800 V bus).
2. **Technology guide:** MOSFET (low voltage up to about 200 V, fast), super-junction MOSFET (500 to 900 V, hard-switching restricted by body diode), IGBT (above about 600 V, lower frequency, tail current), SiC MOSFET (650 V to 3.3 kV, high frequency and temperature), GaN HEMT (up to 650 V, fastest edges, tight gate-voltage limits).
3. **Conduction loss:** `I_rms^2 Rds_on(Tj)` (take the hot value, typically 1.5 to 2 times the 25 C value for silicon); IGBT `Vce0 Iavg + rce Irms^2`.
4. **Switching loss:** `P_sw ~ 0.5 V I (t_r + t_f) f_sw` for a first estimate, plus `Eoss`/`Qrr` terms; use datasheet energy curves at the actual bus voltage and current.
5. **Paralleling:** MOSFETs share current well (positive temp co-efficient); IGBT needs matched Vce and symmetric layout; use individual gate resistors.
6. **Body diode** performance for synchronous topologies.

**Verify:** compute total loss at worst case, then the junction temperature (see converter thermal design) and compare with the maximum rating with margin (for example 125 C continuous design target).

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
