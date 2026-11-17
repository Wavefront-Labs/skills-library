---
id: engineering-technology.electrical-engineering.protection-coordination.motor-protection
name: motor-protection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [49, 50, 66, electrical-engineering, locked-rotor-and-stall-protection, motor-protection, motor-relay, motor-start-supervision, protection-coordination, thermal-overload]
level: practitioner
status: draft
description: "Set motor protection: thermal overload, locked rotor, stall, start counting and unbalance elements on a multifunction relay."
sources:
  - "https://standards.ieee.org/"
  - "https://www.iec.ch/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Motor protection settings

1. **Thermal model (49):** set full load current (FLA), service factor, and the thermal curve below the motor's locked-rotor hot/cold limits; use separate time constants for running and stopped cooling.
2. **Locked rotor / stall:** time at locked-rotor current must stay below the motor's safe stall time (hot); a speed switch or current check distinguishes start from stall.
3. **Short-circuit (50):** set above starting inrush (asymmetrical, often 1.2 to 1.5 x locked-rotor current) and below the minimum fault current.
4. **Unbalance / phase loss (46):** negative-sequence element protects the rotor from heating (negative sequence heating factor roughly `K`).
5. **Start supervision (66):** limit starts per hour and minimum time between starts as given by the motor manufacturer.
6. **Ground fault, undervoltage, RTD** inputs for stator and bearing temperatures.
7. With VFD-fed motors protect via the drive and verify thermal memory use.

**Verify:** draw the motor starting current and thermal limit curve on a time-current plot and confirm the settings sit between them.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
