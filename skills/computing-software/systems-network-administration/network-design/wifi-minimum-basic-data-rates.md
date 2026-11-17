---
id: computing-software.systems-network-administration.network-design.wifi-minimum-basic-data-rates
name: wifi-minimum-basic-data-rates
category: computing-software
field: systems-network-administration
product: network-design
tags: [wireless-design, basic-rates, mandatory-data-rates, airtime, beacon-rate, 802-11b, cell-size]
level: practitioner
status: draft
description: "Tune Wi-Fi mandatory and supported rates: why disabling 1-11 Mbps frees airtime, 12 vs 24 Mbps minimums, effect on cell size and roaming, and legacy client trade-offs."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg.html
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Minimum basic (mandatory) data rates

Beacons, probe responses, broadcasts and multicast are sent at the lowest mandatory (basic) rate.
At 1 Mbps a beacon takes ~2.5 ms of airtime; with several SSIDs and many APs on a channel, management
traffic alone can eat 30-50 % of airtime.

## Recommended settings
| Environment | 2.4 GHz | 5/6 GHz |
|---|---|---|
| Typical enterprise | disable 1, 2, 5.5, 6, 9, 11; mandatory 12, supported 18 and up | mandatory 12 or 24, disable 6 and 9 |
| High density (auditoriums, stadiums) | mandatory 24 | mandatory 24 |
| Warehouses/outdoor with sparse coverage, legacy scanners | keep 6 or 11 if needed | mandatory 6 or 12 |
Disabling 802.11b rates (1/2/5.5/11) on 2.4 GHz also removes protection mechanisms that slow
everyone down.

On a Catalyst 9800 these are per band (RF profile):
```
ap dot11 24ghz rate RATE_1M disable
ap dot11 24ghz rate RATE_11M disable
ap dot11 24ghz rate RATE_12M mandatory
ap dot11 5ghz rate RATE_6M disable
ap dot11 5ghz rate RATE_12M mandatory
```
(Disable the network on the band before changing global rates, or use RF profiles per AP group.)

## Effects
- Smaller effective cells: clients far from the AP cannot decode beacons at 12/24 Mbps, so they
  roam to a closer AP sooner. This reduces sticky-client problems but requires the design to have
  overlapping coverage at the higher rate (-67 dBm design usually supports 24 Mbps).
- Faster broadcasts/multicast (ARP, mDNS) and less airtime per beacon.
- Legacy devices (old 802.11b scanners, some IoT) fail to associate. Inventory first; put legacy on
  a separate SSID/RF profile in the areas where they live.

## Verify
- [ ] Beacon frames in a monitor-mode capture show the expected rate (radiotap data rate), channel
  utilisation drops, and a test of legacy devices in scope passes.
