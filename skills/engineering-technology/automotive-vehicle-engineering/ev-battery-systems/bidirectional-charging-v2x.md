---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.bidirectional-charging-v2x
name: bidirectional-charging-v2x
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [bidirectional-charging, v2g, v2h, v2l, iso-15118-20, anti-islanding, grid-code]
level: practitioner
status: gated
description: "Specify bidirectional charging (V2L, V2H, V2G): onboard or offboard inverter, protocol support, grid-code compliance, battery ageing and warranty effects."
sources:
  - "ISO 15118-20 overview; confirm current edition"
  - "IEC 61851 and grid code references by country"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bidirectional charging V2X

1. Modes: V2L (vehicle to load, standalone AC outlet), V2H (home backup/energy management, vehicle can island a home), V2G (grid export with grid services).
2. Hardware: bidirectional onboard AC charger (DAB stage and bidirectional PFC) or an offboard DC charger/inverter at the wall (DC bidirectional).
3. Communication: ISO 15118-20 (published 2022, per Wikipedia's reference list) adds bidirectional power transfer (gated: unconfirmed, source is paywalled or blocked), dynamic control and scheduled modes; local profiles and charger certification vary by country. Confirm current support in your target charger ecosystem.
4. Grid compliance: anti-islanding detection, ride-through for voltage and frequency, harmonics, protection settings per the national grid code and utility interconnection rules (e.g. IEEE 1547 in the US, EN 50549 in Europe (gated: unconfirmed, source is paywalled or blocked); confirm current versions).
5. Battery: extra cycling raises ageing; set SOC windows and power limits; warranty terms must address V2X usage.
6. Safety: off-grid mode protective earth system and earthing arrangements (TN/TT/IT), residual current protection, safe disconnect.
7. Business: tariffs, aggregator contracts; not an engineering parameter but affects requirements.

**Gotchas:** islanding without a proper earthing concept is dangerous; require certified equipment.

## Verify
- [ ] Test with certified bidirectional charger and grid simulator for anti-islanding and ride-through.
- [ ] Ageing model includes V2X duty.
