---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-mimo-mu-mimo-ofdma
name: wifi-mimo-mu-mimo-ofdma
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-mimo, wifi-ofdma, beamforming-mu-mimo]
level: practitioner
status: draft
description: "Explain how MIMO, MU-MIMO, beamforming and OFDMA use the channel and what clients must support for the benefit."
sources:
  - https://www.ieee802.org/11/
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MIMO, MU-MIMO, beamforming, OFDMA

- MIMO sends multiple spatial streams through multipath reflections. Rate scales with the smaller of AP and client stream counts.
- Beamforming steers energy to a client using client feedback; gains shrink for mobile clients.
- MU-MIMO serves several clients simultaneously (downlink in 802.11ac Wave 2; uplink and downlink in 802.11ax). It needs many MU-capable clients that are spatially separable.
- OFDMA (802.11ax) divides the channel into resource units so several clients, often with small packets, share one transmission: it helps density and latency, not single-client peak speed.
- Both ends must support a feature. Check client capability reports before crediting or blaming a feature.

## Verify
- [ ] Feature is enabled on the controller and visible in capture or vendor dashboards (HE MU/OFDMA frames).
