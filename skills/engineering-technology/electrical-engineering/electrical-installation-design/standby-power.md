---
id: engineering-technology.electrical-engineering.electrical-installation-design.standby-power
name: standby-power
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [ats-and-transfer-schemes, automatic-transfer-switch, battery-autonomy-calculation, electrical-engineering, electrical-installation-design, nec-700, nfpa-110, standby-generator, standby-power, ups-sizing]
level: practitioner
status: draft
description: "Size standby generators, UPS and transfer schemes: ATS selection, battery autonomy and load priority."
sources:
  - "https://www.nfpa.org/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Standby power and UPS design

1. **Classify loads:** life safety (egress lighting, fire pumps), legally required standby, optional standby, critical business loads; NEC Articles 700, 701, 702 define requirements and NFPA 110 covers emergency and standby power systems (check edition).
2. **UPS sizing:** `kVA >= load kVA / (0.8 to 0.9 loading)` with pf (modern units are unity-pf kW=kVA); topology: line-interactive, double-conversion online; include battery autonomy: `Ah = P x t / (V_bat x DoD x eta x aging factor)`, with aging factor about 1.25 and temperature factor.
3. **Example:** 10 kW for 15 min on a 240 V string, DoD 0.8, eta 0.92, aging 1.25: `Ah = 10,000 x 0.25 h /(240 x 0.8 x 0.92) x 1.25 = 17.7 Ah` before discharge-rate (Peukert) correction; use the manufacturer's constant-power tables.
4. **Generator interface:** ATS with open, closed or soft-load transition; delay timers (engine start, transfer, cool down); generator must accept UPS rectifier loading (soft start, harmonic impact).
5. **Selectivity and fault levels** on the generator side are lower than utility; check protection.
6. **Maintenance:** transfer tests monthly, load bank annually, battery impedance testing.

**Verify:** run a full black-start test, recording transfer time and voltage and frequency.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
