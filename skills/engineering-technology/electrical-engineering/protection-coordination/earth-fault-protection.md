---
id: engineering-technology.electrical-engineering.protection-coordination.earth-fault-protection
name: earth-fault-protection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [87n, earth-fault-protection, electrical-engineering, ground-fault-protection, neutral-grounding-resistor-sizing, ngr, protection-coordination, restricted-earth-fault, sensitive-earth-fault-detection]
level: practitioner
status: draft
description: "Design earth-fault protection: neutral grounding resistor sizing, restricted earth fault and sensitive or high-impedance detection."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Earth fault and ground protection

1. **Neutral grounding resistor:** `R = V_LN / I_fault_limit`. Example: 6.6 kV system, 400 A limit: `R = (6600/sqrt(3))/400 = 9.5 ohm`. Rate the resistor for the fault current and time (for example 10 s), and use a CT on the neutral.
2. **Choice:** low-resistance (hundreds of amps) allows selective relaying; high-resistance (under about 10 A) limits damage and lets a single fault persist but requires alarming and rapid location.
3. **Restricted earth fault (87N):** compares the neutral CT current with the residual of the line CTs for a transformer or generator winding; very sensitive to winding earth faults close to the neutral; use a stabilising resistor in high-impedance form.
4. **Core-balance CT:** for feeders, a ring CT encircling all phases gives a sensitive earth fault element; keep cable sheath return paths through the CT correct.
5. **Ungrounded or compensated networks:** directional wattmetric or transient earth-fault detection.
6. Coordinate time grading with the upstream earth-fault element.

**Verify:** injection test pickup and inject through the neutral CT to confirm polarity.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
