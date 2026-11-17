---
id: engineering-technology.electrical-engineering.electrical-installation-design.pv-installation-design
name: pv-installation-design
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [electrical-engineering, electrical-installation-design, iec-62548, nec-690, pv-array-sizing, pv-dc-protection, pv-installation-design, rapid-shutdown, solar-pv, string-sizing-by-temperature]
level: advanced
status: draft
description: "Design solar PV electrical systems: string sizing by temperature, DC protection, rapid shutdown and NEC Article 690 concepts."
sources:
  - "https://www.nfpa.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Solar PV electrical design

1. **String voltage:** maximum open-circuit voltage at the lowest site temperature `Voc_max = N Voc_stc (1 + beta_Voc (Tmin - 25))` (beta negative; use the module datasheet) must stay below the inverter and module system voltage limit (1000 V, 1500 V). Minimum string MPP voltage at the highest cell temperature must exceed the inverter MPPT minimum.
2. **Strings per MPPT:** current limit of the MPPT input versus `Isc` times 1.25 (NEC 690.8 uses 125 percent of Isc, and another 125 percent for continuous loading; check the adopted edition).
3. **DC protection:** PV-rated fuses, DC isolators, arc-fault detection where required (NEC 690.11), and surge protection.
4. **Rapid shutdown (NEC 690.12):** requirements for rooftop arrays are specified (module-level shutdown for many editions); consult the edition adopted.
5. **Cables:** PV wire (USE-2, PV Wire; H1Z2Z2-K in Europe), UV-resistant, 90 C wet rating, voltage drop below 1 to 2 percent on DC.
6. **Grounding and bonding** of module frames and racking (UL 2703 or equivalent), and equipment grounding conductors.
7. **AC side:** inverter output breaker at 125 percent of inverter current, interconnection rule (120 percent busbar rule in NEC 705.12).

**Verify:** string Voc and Isc measurement at commissioning (IEC 62446-1), with insulation resistance tests.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
