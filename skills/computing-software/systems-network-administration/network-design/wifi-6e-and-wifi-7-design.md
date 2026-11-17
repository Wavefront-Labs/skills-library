---
id: computing-software.systems-network-administration.network-design.wifi-6e-and-wifi-7-design
name: wifi-6e-and-wifi-7-design
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, multi-link-operation, wifi-6e, wifi-7, 6-ghz, wpa3, 320-mhz]
level: practitioner
status: draft
description: "Design for Wi-Fi 6E and Wi-Fi 7: 6 GHz rules (WPA3 only, PSC channels, AFC), channel widths, multi-link operation, AP uplinks and client readiness."
sources:
  - https://www.wi-fi.org/discover-wi-fi/wi-fi-certified-7
  - https://www.wi-fi.org/discover-wi-fi/wi-fi-certified-6
  - https://www.cisco.com/c/en/us/products/collateral/wireless/catalyst-9100ax-access-points/wi-fi-7-wp.html
  - https://www.fcc.gov/document/fcc-opens-6-ghz-band-wi-fi-and-other-unlicensed-uses
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wi-Fi 6E and Wi-Fi 7 design

## 6 GHz basics (Wi-Fi 6E)
- Up to 1200 MHz of spectrum (US; Europe 500 MHz lower 6 GHz): 59 x 20 MHz, 14 x 80 MHz,
  7 x 160 MHz, 3 x 320 MHz (Wi-Fi 7).
- **WPA3 (or OWE for open) is mandatory**; no WPA2, no TKIP. Existing WPA2/WPA3 transition SSIDs
  need a WPA3-only 6 GHz variant or a separate SSID.
- Client discovery: no probe-flooding; clients find 6 GHz via Reduced Neighbor Reports in 2.4/5 GHz
  beacons, FILS discovery, or by scanning the 15 **Preferred Scanning Channels** (PSC, every 4th
  20 MHz channel). Put 80/160 MHz primaries on PSCs.
- Power classes: Low Power Indoor (no AFC), Standard Power (AFC database required, outdoors),
  Very Low Power. Indoor LPI EIRP is low; 6 GHz attenuates more through walls, so cell size is
  roughly like 5 GHz at matched power but plan from a survey.

## Wi-Fi 7 (802.11be)
- **Multi-Link Operation (MLO)**: one client association across 2.4/5/6 GHz links with the same
  SSID, security and MLD MAC. Modes: STR (simultaneous transmit/receive), eMLSR (listen on several,
  transmit on one). Requires all links of an SSID to use WPA3 and matching settings (AKM, PMF).
- 320 MHz channels, 4096-QAM, preamble puncturing (use wide channels despite one busy 20 MHz).
- MLO gives reliability/latency gains more than raw speed in enterprise; do not plan on 320 MHz
  in multi-AP deployments (only 3 channels).

## Wired side
- APs need mGig: 2.5G for 6E, 5G/10G for Wi-Fi 7, and 802.3bt PoE for full radios (some degrade
  on at-power).
- Uplinks from IDF switches sized for the new AP aggregate.

## Plan
1. Survey 6 GHz specifically (AP-on-a-stick); expect denser AP grid than a 2.4 GHz-era design.
2. 20/40 MHz on 5 GHz in dense areas, 80 MHz on 6 GHz (160 where few APs).
3. Inventory clients: 6E/7 capability, OS/driver versions; MLO support varies widely.

## Verify
- [ ] Clients discover and roam on 6 GHz (RNR present), WPA3-SAE/802.1X works, MLO clients show multiple active links.
