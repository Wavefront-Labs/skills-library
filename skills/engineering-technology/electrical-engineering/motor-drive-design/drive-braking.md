---
id: engineering-technology.electrical-engineering.motor-drive-design.drive-braking
name: drive-braking
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [active-front-end, brake-chopper, brake-resistor-sizing, dc-bus-overvoltage-management, drive-braking, dynamic-braking, electrical-engineering, motor-drive-design, regenerative-drive]
level: practitioner
status: draft
description: "Size braking resistors and manage DC bus overvoltage in VFDs, including regenerative front ends."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Drive braking and regeneration

1. **Energy to dissipate:** deceleration energy `E = 0.5 J (w1^2 - w2^2)` minus losses; braking power `P_brake = T_brake w`; for overhauling loads (cranes, downhill conveyors) continuous braking power equals load power.
2. **Resistor value:** `R <= Vbrake^2 / P_peak` where Vbrake is the chopper threshold (for a 400 V class drive, often around 750 to 800 V, from the drive manual) and R must be not lower than the drive's minimum resistance. Rate power with duty cycle and thermal time constant.
3. **Protect:** thermal overload on the resistor, enclosure ventilation, and a trip on chopper failure; resistors reach high surface temperature.
4. **Alternatives:** extend deceleration time; DC-bus braking in the motor (flux braking); common DC bus so one drive's regeneration feeds another; regenerative / active-front-end drives return energy to the grid but need harmonic and anti-islanding considerations.
5. Avoid overvoltage trips by enabling the DC link overvoltage controller (automatically lengthens ramp).

**Verify:** record DC bus voltage during the worst deceleration and confirm it remains under the trip level with margin.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
