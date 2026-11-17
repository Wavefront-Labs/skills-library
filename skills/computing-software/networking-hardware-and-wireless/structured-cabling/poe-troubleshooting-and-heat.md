---
id: computing-software.networking-hardware-and-wireless.structured-cabling.poe-troubleshooting-and-heat
name: poe-troubleshooting-and-heat
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [poe-troubleshooting, poe-cable-heating, poe-overload]
level: practitioner
status: draft
description: "Diagnose PoE devices that will not power, reboot or negotiate low power, and manage cable heating in large bundles."
sources:
  - https://www.ieee802.org/3/
  - https://tiaonline.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PoE faults

- No power: check detection signature (PD resistance), PoE enabled on port, budget exhausted, cable pair breaks (a failed pair on a 4-pair bt link).
- Reboot loops: power budget overcommit or inrush; cap with per-port limits and priority, raise total budget with a larger PSU or power supply units.
- Negotiated lower class: device asked for 802.3at but switch grants af; check negotiation settings and firmware.
- Heat: high-power PoE in tightly bundled cable raises conductor temperature and attenuation; keep bundles small, use Cat6A/larger gauge cable, and consult TIA TSB-184-A guidance.
- Surge protection: outdoor PoE runs need surge protectors and bonding.

## Verify
- [ ] PD stays powered across a 24-hour soak at peak load; no event logs for power denial.
