---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-mcs-and-guard-interval
name: wifi-mcs-and-guard-interval
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-mcs-index, guard-interval, spatial-streams]
level: practitioner
status: draft
description: "Decode an MCS index into modulation, streams and width and explain why rate drops with distance."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading MCS, NSS, width and guard interval

- An MCS index fixes modulation and coding rate. Higher MCS packs more bits per symbol (256-QAM in 802.11ac, 1024-QAM in 802.11ax, 4096-QAM in 802.11be) and needs higher SNR.
- Rate is a function of MCS, NSS (spatial streams), channel width and guard interval. Doubling width roughly doubles rate but raises the noise floor about 3 dB.
- Shorter guard intervals add rate but tolerate less multipath delay spread; 802.11ax added longer GI options for reflective spaces.
- Rate adaptation is vendor-specific. At the cell edge a client steps MCS down; low-MCS frames occupy more airtime and slow every client in the cell.

## Tools
- Linux: `iw dev wlan0 link` shows `tx bitrate` with MCS, NSS and GI.
- Windows: `netsh wlan show interfaces` shows radio type and transmit/receive rate.

## Verify
- [ ] Reported MCS/NSS is consistent with the client's capabilities; a 2-stream client never shows 3-stream rates.
