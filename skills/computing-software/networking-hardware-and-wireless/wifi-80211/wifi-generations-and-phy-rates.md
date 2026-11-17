---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-generations-and-phy-rates
name: wifi-generations-and-phy-rates
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-generations, wifi-phy-rates, 80211-amendments, wifi-standards-generations]
level: intro
status: draft
description: "Map Wi-Fi generations to 802.11 amendments and bands, and explain why PHY rate is not throughput."
sources:
  - https://www.ieee802.org/11/
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wi-Fi generations and what they mean on the wire

| Marketing name | Amendment | Bands |
|---|---|---|
| Wi-Fi 4 | 802.11n | 2.4 / 5 GHz |
| Wi-Fi 5 | 802.11ac | 5 GHz only |
| Wi-Fi 6 | 802.11ax | 2.4 / 5 GHz |
| Wi-Fi 6E | 802.11ax | adds 6 GHz |
| Wi-Fi 7 | 802.11be | 2.4 / 5 / 6 GHz |

- PHY rate is the modulation ceiling, not throughput. Real TCP throughput is typically about half of PHY rate or less (contention, preambles, ACKs, retries).
- Rate depends on channel width, modulation (MCS), spatial streams and guard interval. Phones and laptops are commonly 2x2; do not size from 4x4 AP marketing numbers.
- The client usually sets the ceiling. Check its Wi-Fi generation, streams and 6 GHz support before promising speeds.
- Legacy support costs airtime: disable low basic rates (1/2/5.5/11 Mbps on 2.4 GHz) when no legacy clients exist.

## Verify
- [ ] Read the client's actual link rate/MCS/NSS from its OS diagnostics, not the AP's advertised maximum.
- [ ] Confirm the AP SKU supports the bands you need (6 GHz is regional and SKU-specific).
