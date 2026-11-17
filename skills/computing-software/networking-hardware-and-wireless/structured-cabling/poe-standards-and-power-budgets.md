---
id: computing-software.networking-hardware-and-wireless.structured-cabling.poe-standards-and-power-budgets
name: poe-standards-and-power-budgets
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [poe-802-3at-bt, poe-power-budget, poe-class, cabling-poe]
level: practitioner
status: draft
description: "Plan PoE classes and total budgets: PSE vs PD power, cable loss, 4-pair power and how to sum worst-case draw."
sources:
  - https://www.ieee802.org/3/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PoE planning

- 802.3af (Type 1): 15.4 W at PSE, 12.95 W at PD. 802.3at (Type 2, PoE+): 30 W / 25.5 W. 802.3bt Type 3: 60 W / 51 W; Type 4: 90-100 W / 71.3 W. Always check the PSE vs PD figure (cable loss).
- 802.3bt uses all four pairs; af/at use two (alternative A or B).
- Total switch PoE budget limits the number of powered ports; sum worst-case PD draw (cameras with heaters/IR, APs) not average.
- Class negotiation can use hardware classification or LLDP power negotiation.
- Passive PoE (non-standard, e.g. some Ubiquiti models) does not negotiate; connecting it to a standard device can destroy ports. Check the device's required PoE type.

## Verify
- [ ] Switch `show power inline` (or equivalent) lists budget used with headroom.
