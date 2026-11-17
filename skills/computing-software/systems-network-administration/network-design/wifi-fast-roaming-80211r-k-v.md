---
id: computing-software.systems-network-administration.network-design.wifi-fast-roaming-80211r-k-v
name: wifi-fast-roaming-80211r-k-v
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, wifi-design, fast-roaming, 802-11r, 802-11k, 802-11v, ft, okc, pmk-caching, bss-transition, neighbor-report, sticky-client, roaming-thresholds, adaptive-ft]
level: practitioner
status: docs-checked
description: "Enable fast roaming correctly: 802.11r FT (and its client compatibility trap), OKC/PMK caching, 802.11k neighbour reports and 802.11v BSS transition, plus how to test roam times."
sources:
  - https://support.apple.com/guide/deployment/wi-fi-roaming-support-dep98f116c0f/web
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fast roaming: 802.11r, k and v

Clients decide when and where to roam; the network can only make roaming **faster** and **better informed**.

## The amendments (as Apple describes them for managed networks)
| Feature | Purpose |
|---|---|
| 802.11r Fast BSS Transition (FT) | helps devices quickly and securely roam between access points |
| PMKID caching | fast roaming back to previously associated access points |
| 802.11k Radio Measurement | delivers the list of neighbouring access points |
| 802.11v Wireless Network Management | helps identify the optimal access point for roaming |

On Cisco networks, Adaptive 802.11r lets Apple devices that support FT coexist with legacy devices that do not.

## Configuration guidance
- Some older clients (printers, scanners, old drivers) may fail to join SSIDs that advertise FT: test them, or put them
  on a separate SSID, or use the vendor's adaptive FT mode where it exists.
- Enable 802.11k and 802.11v on voice and enterprise SSIDs, and verify client behaviour; clients decide whether to act
  on suggestions.
- Fast roaming only works between APs that share the key hierarchy (same controller or roaming domain); confirm the
  domain boundaries in your vendor's configuration guide.
- Check your controller vendor's configuration guide for exact modes and defaults (the Cisco 9800 page cited under
  `sources` is an index page in the fetched copy).

## Test roam times
- Monitor-mode capture: time from the last data frame on the old BSSID to the first data frame on the new BSSID, and
  whether a full 802.1X exchange occurs on the roam.
- Controller client roaming history.
- Voice test: a continuous call while walking a planned route; compare loss and quality per roam.

## Verify
- [ ] Roams on the 802.1X SSID complete without a full EAP exchange and without audible glitches.
- [ ] Legacy devices still connect (separate SSID if needed).
- [ ] 802.11k/v enabled and visible in beacons/association responses.

## Checked
2026-10-28. Confirmed in Apple's "Wi-Fi roaming support" page: the purpose of 802.11r, PMKID caching, 802.11k, 802.11v
and Cisco Adaptive 802.11r. Removed as unconfirmed: roam-time figures (ms), OKC description, WPA3 FT details, FT mode
names, the Wireshark display filter, the WLC command, the 50 ms pass threshold, over-the-air versus over-the-DS advice.
The Cisco 17-9 deep link returned 404 and was dropped from `sources`.
Method: documentation only; no commands were run.
