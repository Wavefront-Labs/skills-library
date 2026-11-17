---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-6ghz-psc-and-afc
name: wifi-6ghz-psc-and-afc
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-6ghz, afc-standard-power, psc-channels]
level: advanced
status: draft
description: "Plan Wi-Fi 6E/7 6 GHz channels: preferred scanning channels, low-power indoor versus AFC standard power, and mandatory WPA3."
sources:
  - https://www.ieee802.org/11/
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 6 GHz (Wi-Fi 6E / Wi-Fi 7)

- Large new spectrum (5925-7125 MHz where fully opened); wide channels (160 MHz, and 320 MHz in 802.11be) become practical. Availability is regional.
- Preferred Scanning Channels (PSC): every fourth 20 MHz channel is a PSC; clients scan these first, so 6 GHz SSIDs are discovered faster. 6 GHz SSIDs are also advertised in Reduced Neighbor Report elements in 2.4/5 GHz beacons.
- 6 GHz requires WPA3-SAE or Enhanced Open (OWE); WPA2-PSK-only and legacy open are not allowed there. Plan SSIDs accordingly.
- Power classes: Low Power Indoor (LPI) is simplest. Standard Power requires Automated Frequency Coordination (AFC) in regions that adopted it (confirm status in your country and AP certification).

## Verify
- [ ] Client supports 6 GHz in your regulatory domain (not every Wi-Fi 6 client is 6E).
- [ ] The 6 GHz SSID uses SAE/OWE and clients actually associate on that band.
