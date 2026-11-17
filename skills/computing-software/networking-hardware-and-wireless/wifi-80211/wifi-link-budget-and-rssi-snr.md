---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-link-budget-and-rssi-snr
name: wifi-link-budget-and-rssi-snr
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-link-budget, rssi-snr, noise-floor, wifi-rf-fundamentals]
level: practitioner
status: draft
description: "Calculate link budget from EIRP and path loss, and set coverage targets using RSSI and SNR."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Link budget, RSSI and SNR

- EIRP = transmit power (dBm) + antenna gain (dBi) - cable loss (dB). Regulators cap EIRP per band and country.
- SNR = signal (dBm) - noise floor (dBm). A typical indoor noise floor is roughly -90 to -95 dBm; interference raises it.
- Commonly cited design targets (starting points, not standards): about -67 dBm for voice/video-grade coverage, about -70 dBm for data, SNR of 25 dB or better at the cell edge for high MCS.
- Free-space path loss grows 6 dB per doubling of distance and with frequency (5 GHz loses more than 2.4 GHz). Walls and people add attenuation; measure rather than assume.
- 3 dB = double/half power, 10 dB = 10x. Learn the 3/6/10 rules.
- Design for the client's uplink: a phone at roughly 15 dBm cannot answer an AP at 23 dBm at the same range.

## Verify
- [ ] Surveyed RSSI/SNR at the cell edge meets the application target.
