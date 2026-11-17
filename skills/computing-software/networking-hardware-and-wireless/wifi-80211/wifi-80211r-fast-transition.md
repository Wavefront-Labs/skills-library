---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-80211r-fast-transition
name: wifi-80211r-fast-transition
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-80211r, fast-bss-transition, pmk-caching, wifi-roaming]
level: advanced
status: draft
description: "Enable 802.11r FT (over-the-air or over-DS) with correct mobility domain and key holders so voice clients roam fast."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 802.11r (FT)

- FT precomputes keys so a roam skips a full 802.1X exchange. Requires a shared mobility domain ID and key hierarchy across APs on the same SSID (controller or cluster handles it).
- Modes: over-the-air (client talks to target AP directly) and over-DS (via the current AP). Over-the-air is more broadly compatible.
- Some older clients fail to associate to FT-enabled SSIDs ("FT adaptive" or mixed modes exist on some platforms). Test device classes, especially IoT and printers.
- Alternatives when FT is unsuitable: OKC/PMK caching (vendor-specific, non-standard) or sticky roam avoidance.

## Verify
- [ ] Capture shows Reassociation Request with FT elements and no full EAP exchange.
- [ ] A voice call holds through a walk test with sub-50-ms gaps (confirm your threshold).
