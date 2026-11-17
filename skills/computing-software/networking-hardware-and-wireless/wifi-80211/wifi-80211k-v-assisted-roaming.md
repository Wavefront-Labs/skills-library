---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-80211k-v-assisted-roaming
name: wifi-80211k-v-assisted-roaming
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-80211k, wifi-80211v, bss-transition-management]
level: practitioner
status: draft
description: "Enable 802.11k neighbor reports and 802.11v BSS transition management so clients choose better APs and sticky clients move."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 802.11k and 802.11v

- 802.11k gives the client a neighbour list from the AP so it scans fewer channels. 802.11v lets the AP suggest (BSS Transition Management request) a better AP.
- Clients decide; 802.11v is a request, not a command. Many clients honour it, some ignore it.
- Sticky clients (staying on a distant AP) are the usual complaint. Fix by combining correct cell sizing (see RF skills), 802.11k/v, and minimum RSSI/basic rate thresholds, not by forced disconnects.
- Aggressive client-kick at RSSI thresholds can cause roam loops; use hysteresis and test.

## Verify
- [ ] A packet capture shows Neighbor Report Request/Response and BSS Transition Request frames.
