---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.hv-fusing-and-contactor-protection
name: hv-fusing-and-contactor-protection
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [hv-fusing, fuse, pyro-fuse, short-circuit, breaking-capacity, i2t, hv-protection]
level: practitioner
status: gated
description: "Select HV fuses and coordinate them with contactors and cables: rated voltage, breaking capacity, I2t, time-current curves and pyro-fuse use."
sources:
  - "fuse manufacturer application guides (Littelfuse, Eaton, Mersen)"
  - "ISO 6469-3 protection requirements; confirm edition"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# HV fusing and contactor protection

1. Determine prospective short-circuit current: `Vpack/(R_internal + R_wiring)`; use minimum resistance (new pack, warm) and highest voltage. It can reach several kA to tens of kA (gated: unconfirmed, source is paywalled or blocked).
2. Fuse selection: DC voltage rating above the maximum pack voltage; interrupt (breaking) capacity above the prospective current; continuous rating with derating for temperature and cycling; time-current curve below the cable and busbar damage curve and above the normal peak current including inrush.
3. Coordination: the fuse must clear a fault before the contactor is damaged; contactor breaking capacity covers the lower fault currents; below that, the BMS opens the contactor by overcurrent detection.
4. Pyro fuses (pyrotechnic disconnect) act on a crash signal, interrupting under current with a ms-scale trigger (gated: unconfirmed, source is paywalled or blocked); they are single-use.
5. Place fuses to protect branches (HVAC, charger, DC-DC) as well as the pack main.
6. Test: short-circuit test at the pack level with the intended source impedance.
7. Document the protection concept for the safety case.

**Gotchas:** AC-rated fuses used on DC; ageing of fuse elements from thermal cycling.

## Verify
- [ ] Fuse interrupt rating above computed worst-case fault current with margin.
- [ ] Short-circuit test shows fuse clears without contactor damage.
