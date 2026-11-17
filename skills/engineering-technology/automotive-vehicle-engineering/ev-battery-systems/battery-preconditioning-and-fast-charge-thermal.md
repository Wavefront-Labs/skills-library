---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.battery-preconditioning-and-fast-charge-thermal
name: battery-preconditioning-and-fast-charge-thermal
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [battery-preconditioning, preconditioning, fast-charge-thermal, cold-charging, heater, heat-pump, plating-risk]
level: practitioner
status: gated
description: "Plan battery thermal preconditioning before DC fast charge and in cold weather: target temperatures, heating options, navigation trigger and plating risk."
sources:
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
  - "Plett, Battery Management Systems Vol. 1"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Preconditioning and fast-charge thermal

1. Why: fast charging at low temperature risks lithium plating and is power-limited by the BMS; at high temperature it accelerates ageing and may need throttling.
2. Target window: warm the pack toward the cell supplier's recommended fast-charge range (commonly in the 20-40 C region (gated: unconfirmed, source is paywalled or blocked); use datasheet values).
3. Heating options: coolant heater (PTC or high-voltage heater), heat pump, motor/inverter waste heat, self-heating by AC ripple current (needs development), insulation.
4. Trigger: navigation to a fast charger starts conditioning on arrival time; manual preconditioning option; plugged-in conditioning to save battery energy.
5. Energy budget: heating a 500 kg pack by 20 K needs `m*cp*dT` (500 kg x about 1 kJ/(kg K) x 20 = 10 MJ, about 2.8 kWh, computed 2.78 kWh) before losses, so timing matters.
6. Cooling: during charge, remove heat with chiller/refrigerant loop; stage charging power to stay below limits.
7. Validate in climate chamber at -20, 0, 25 and 40 C: charge time and maximum temperature.

**Gotchas:** pack thermal mass and insulation make warm-up slow; model it.

## Verify
- [ ] 10-80% charge time at each temperature with and without preconditioning logged.
- [ ] No charge current above the BMS temperature-dependent limit.
