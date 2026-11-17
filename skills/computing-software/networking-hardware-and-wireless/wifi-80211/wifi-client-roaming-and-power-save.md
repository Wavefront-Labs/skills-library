---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-client-roaming-and-power-save
name: wifi-client-roaming-and-power-save
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-client-behaviour, mac-address-randomisation, wifi-power-save, wifi-clients-iot]
level: practitioner
status: draft
description: "Plan around client-side decisions: roam triggers, power-save modes (including TWT) and per-SSID MAC randomisation that breaks MAC allow-lists."
sources:
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client behaviour you do not control

- The client decides when to roam; AP-side settings only influence it. Phones, laptops and scanners differ widely, so test each device class.
- Power save: DTIM interval and listen interval trade battery for latency; long DTIM delays multicast/ARP delivery. 802.11ax Target Wake Time (TWT) schedules wake times for IoT.
- Modern OSes use randomised MAC addresses per SSID by default. MAC-based allow-lists, DHCP reservations and usage analytics then break; use certificates or per-device keys instead of MAC identity.
- Check supported bands/capabilities in the association request (HT/VHT/HE capabilities) to see what the client actually supports.

## Verify
- [ ] A test device's behaviour with randomised and fixed MAC is documented, and policies do not rely on a stable MAC.
