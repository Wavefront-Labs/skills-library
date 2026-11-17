---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-interference-and-spectrum-analysis
name: wifi-interference-and-spectrum-analysis
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-spectrum-analysis, non-wifi-interference, duty-cycle]
level: advanced
status: draft
description: "Use a spectrum analyser to identify non-Wi-Fi interferers by signature and duty cycle and decide between moving channels or removing the source."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spectrum analysis

- A Wi-Fi radio cannot see non-Wi-Fi energy except as raised noise or CRC errors. A spectrum analyser shows FFT, duty cycle and swept spectrograms.
- Signatures: microwave ovens (wide band around the 2.4 GHz upper part, pulsing), analog video cameras (continuous narrow carrier), Bluetooth/ZigBee (hopping), radar in DFS bands.
- Duty-cycle matters more than peak: a 10 percent duty-cycle source may barely affect a channel; a 90 percent one kills it.
- Remedies: change channel/band, move or shield the source, or replace device.

## Verify
- [ ] After remediation, channel utilisation and retry rates fall in a repeat measurement.
