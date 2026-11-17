---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.quiescent-current-budget
name: quiescent-current-budget
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [quiescent-current, sleep-current, parked-drain, battery-drain, current-budget, 12v-battery, standby-current, power-distribution, ecu-sleep, parasitic-draw]
level: practitioner
status: gated
description: "Build and verify a quiescent (parked) current budget: per-ECU limits, battery energy arithmetic, measurement procedure, and common causes of drain."
sources:
  - "Navet and Simonot-Lion, Automotive Embedded Systems Handbook (chapter list)"
  - "OEM electrical requirements documents for quiescent current (company-specific; confirm limits)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Quiescent current budget

## 1. Why budget
A parked vehicle must start after weeks of standby, and under connected-car and security features the baseline drain is rising. A budget allocates the allowable total to each ECU and function.

## 2. Arithmetic
Usable energy for parked drain = battery capacity (Ah) x usable fraction x temperature and ageing factor. Example (illustrative, replace with your numbers): a 60 Ah 12 V lead-acid battery, keep enough to start, so assume 12 Ah usable at end of life; with a total sleep current of 30 mA the standby period is 12 / 0.030 = 400 hours, about 16.7 days. If the requirement is 30 days, the budget is 12 / 720 = 16.7 mA. Include periodic activities (telematics checks, thermal management, key search) as an average: I_avg = sum(I_k x t_k)/T.

## 3. Allocation
Total vehicle limit (OEM-specific; a few tens of milliamps is commonly quoted for conventional vehicles (gated: unconfirmed, source is paywalled or blocked), lower for long-storage requirements) divided among ECUs; typical ECU sleep budgets are on the order of tens to a few hundred microamps each (check your OEM spec (gated: unconfirmed, source is paywalled or blocked)), while always-on functions (telematics, alarm, remote keyless entry receivers) have larger allowances. Record budget and measured values in a table and update it at each design stage.

## 4. Measurement procedure
1. Put the vehicle in the defined parked state: doors closed, key removed or out of range, latches in the locked state, accessories off, bus recorder attached.
2. Insert a current measurement in the battery negative lead with a shunt or a fast current probe (do not interrupt the circuit with a low-range ammeter while loads wake; use a bypass and high dynamic range).
3. Wait until all ECUs sleep (observe bus traffic stop; this can take tens of minutes), then record for a defined period and capture wake events.
4. Repeat at temperature extremes and after a simulated user pattern (door opened, lock cycles).
5. Break down by pulling fuses one at a time or by using per-circuit current clamps, to attribute current to circuits.

## 5. Common causes
Missing sleep handshake, a node that does not release NM, wake line leakage (moisture in connector), pull-up resistors to battery, transceivers not in standby, regulators with high quiescent current, LEDs or sensors fed permanently, and software loops that keep a processor awake. Add design rules: low-Iq regulators, switched supplies for non-critical circuits, and standby mode of microcontrollers.

## Verify
- [ ] Budget table with per-ECU values and measured data.
- [ ] Arithmetic includes ageing, temperature and periodic activities.
- [ ] Measurement method records time to sleep and wake events.
- [ ] Outliers traced and closed with a design change or exception.
