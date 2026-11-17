---
id: computing-software.systems-network-administration.network-design.wifi-channel-planning
name: wifi-channel-planning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, wifi-design, channel-planning, channel-width, 2-4ghz, 5ghz, 6ghz, dfs, co-channel-interference, transmit-power, rrm, psc-channels, wifi-6e, wifi-7, high-density-wifi]
level: practitioner
status: draft
description: "Plan Wi-Fi channels and widths: 1/6/11 on 2.4 GHz, 5 GHz UNII bands and DFS, 6 GHz PSC channels, 20/40/80/160 MHz trade-offs, transmit power balance and RRM settings."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/technotes/8-3/b_RRM_White_Paper.html
  - https://www.comptia.org/certifications/network
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wi-Fi channel planning

The goal is minimal **co-channel contention**: APs that hear each other on the same channel
share airtime as if they were one AP.

## 2.4 GHz
- Only three non-overlapping 20 MHz channels: **1, 6, 11** (1, 5, 9, 13 where ETSI allows, but
  mixing plans with neighbours causes adjacent-channel interference).
- Never 40 MHz in 2.4 GHz.
- In dense deployments, disable 2.4 GHz on a share of APs (or make them monitor/5 GHz dual) so
  the 2.4 cells are not all overlapping. Leave it for IoT and legacy clients.

## 5 GHz
- ~25 x 20 MHz channels (region-dependent) across UNII-1 (36-48), UNII-2 (52-64, DFS),
  UNII-2e (100-144, DFS), UNII-3 (149-165).
- **DFS** channels must vacate on radar detection (1 min channel availability check, client
  disconnects on a hit). Near airports/weather radar, exclude affected channels after observing
  logs; otherwise use them to get more channels.
- Width: 20 MHz for high density (more channels = less reuse), 40 MHz typical office, 80 MHz only
  where AP density is low and channels plentiful.

## 6 GHz (Wi-Fi 6E/7)
- Up to 59 x 20 MHz, 14 x 80, 7 x 160 MHz (US; Europe has the lower 480 MHz only).
- **Preferred Scanning Channels (PSC)**: every 4th 20 MHz channel (5, 21, 37 ...). Clients scan
  only PSCs passively; put APs there or enable discovery in 2.4/5 GHz beacons (RNR).
- WPA3 is mandatory; OWE for open networks.
- 80 MHz is often practical; 160/320 MHz for low-density or specific high-throughput rooms.

## Power
- Balance AP transmit power with **client** power: a phone transmits ~12-15 dBm. An AP at full
  power (20+ dBm) attracts clients that cannot talk back well (asymmetric link). Typical office:
  5 GHz 11-17 dBm, 2.4 GHz 3-6 dB lower than 5 GHz so clients prefer 5 GHz.
- Let RRM/RF profiles (Cisco RRM, Aruba ARM, Mist RRM) assign channels and power within limits
  you set (allowed channel list, min/max power, width).

## Verify
- [ ] Post-deployment survey shows each location hears no more than 1-2 APs on the same channel at > -85 dBm.
- [ ] Allowed channel lists exclude problem DFS channels; widths match density.
- [ ] Clients predominantly on 5/6 GHz.
