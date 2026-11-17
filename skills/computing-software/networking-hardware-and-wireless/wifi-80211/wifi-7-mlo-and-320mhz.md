---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-7-mlo-and-320mhz
name: wifi-7-mlo-and-320mhz
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-7-mlo, preamble-puncturing, 320mhz-channel, wifi-7-features]
level: advanced
status: draft
description: "Understand Wi-Fi 7 multi-link operation, 320 MHz in 6 GHz, 4096-QAM and puncturing and what they need from clients and cabling."
sources:
  - https://www.wi-fi.org/
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wi-Fi 7 essentials

- Multi-Link Operation (MLO): a client uses multiple bands/links concurrently (aggregating or switching) for throughput and lower latency. Needs MLO-capable client and AP; gains depend on mode and traffic.
- 320 MHz channels exist only in 6 GHz and are scarce in dense environments; a 160 MHz design is more realistic in enterprise.
- 4096-QAM raises peak rate but needs very high SNR, so it appears only at close range.
- Preamble puncturing lets a wide channel avoid a narrow interfered sub-channel instead of dropping to a narrower width.
- AP uplinks: plan 5/10 GbE and PoE bt (see AP uplink skill). Features and certifications are rolling out in phases; check the Wi-Fi Alliance certification release for exact capabilities.

## Verify
- [ ] Capture or client stats confirm EHT rate and MLO links in use on a Wi-Fi 7 client.
