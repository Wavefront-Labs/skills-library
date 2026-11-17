---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-wired-uplink-and-poe-for-aps
name: wifi-wired-uplink-and-poe-for-aps
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-ap-uplink, ap-poe-requirements, multigig-uplink]
level: practitioner
status: draft
description: "Match Wi-Fi 6/7 AP power draw to 802.3at/bt PoE budgets and choose multigig uplinks and cable category."
sources:
  - https://www.wi-fi.org/
  - https://www.ieee802.org/3/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AP uplinks and PoE

- Many Wi-Fi 6/7 APs need 802.3at (PoE+, up to 30 W at the PSE) or 802.3bt (PoE++, up to 60/90 W). Running on lower power makes the AP disable radios or chains; check the datasheet's power table.
- Use 2.5GBASE-T or 5GBASE-T (802.3bz) uplinks so a single gigabit link is not the bottleneck; Cat6 or better supports 2.5/5G to 100 m in typical cases, Cat6A for 10G.
- Budget the switch PoE power in total, not per port: sum worst-case AP draw and keep reserve.
- LLDP-MED / power negotiation can reduce a class if misconfigured; confirm allocated vs requested power in the switch.

## Verify
- [ ] The switch shows the AP at the expected PoE class and the AP reports no reduced-power warning.
