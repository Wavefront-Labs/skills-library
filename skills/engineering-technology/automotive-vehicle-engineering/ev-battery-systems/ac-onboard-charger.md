---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.ac-onboard-charger
name: ac-onboard-charger
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [onboard-charger, obc, ac-charging, pfc, llc-converter, control-pilot, j1772, iec-61851, ev-charging]
level: practitioner
status: gated
description: "Design or specify an AC onboard charger: power levels, PFC and isolated DC-DC stages, control pilot signalling, efficiency, grid interaction and safety."
sources:
  - "Mohan, Undeland and Robbins, Power Electronics"
  - "SAE J1772 and IEC 61851-1 overviews; confirm current editions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# AC onboard charger

1. Power by supply: single-phase 230 V 32 A gives about 7.4 kW; three-phase 400 V 16 A about 11 kW; 400 V 32 A about 22 kW (Europe) (computed: 7.36, 11.09, 22.17 kW). US residential single-phase 240 V up to about 19 kW at 80 A (computed 19.2 kW), common levels 7-11 kW.
2. Topology: EMI filter, rectifier + power-factor-correction boost stage, DC link, isolated DC-DC stage (LLC, phase-shifted full bridge, or dual-active bridge if bidirectional), output filter to the HV battery.
3. Targets: peak efficiency in the low-to-mid 90s % and power factor above 0.99 (gated: unconfirmed, source is paywalled or blocked), THD within grid standards, galvanic isolation, leakage current limits (DC leakage detection per the standards).
4. Control pilot (J1772 / IEC 61851): a 1 kHz PWM from the EVSE; duty cycle 10-85% encodes available current `I = duty(%) x 0.6 A` (J1772 table via Wikipedia: 10% = 6 A, 16% = 9.6 A, 85% = 51 A; 85-96% uses a different formula); the vehicle signals state via resistor on the pilot line; proximity pilot signals the plug and cable rating.
5. Grid codes: harmonics, flicker, behaviour on grid faults and phase loss in 3-phase.
6. Thermal: cold plate sizing for losses (for 7.4 kW at 94% about 470 W).
7. Safety: protective earth monitoring, isolation, HV interlock.

**Gotchas:** phase-switching, single-phase fallback, power derating at high temperature.

## Verify
- [ ] Efficiency and PF measured at several loads.
- [ ] Pilot signalling tested with an EVSE simulator including fault states.
