---
id: computing-software.systems-network-administration.network-design.ssid-count-and-beacon-overhead
name: ssid-count-and-beacon-overhead
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, ssid-overhead, beacon-interval, airtime, ssid-design]
level: practitioner
status: gated
description: "Keep SSID count low: calculate beacon airtime overhead per channel, consolidate SSIDs with dynamic VLAN/role assignment, and tune minimum data rates."
sources:
  - https://www.revolutionwifi.net/revolutionwifi/p/ssid-overhead-calculator.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/technical-reference/c9800-best-practices.html
  - https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/Multi-SSID_Deployment_Considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSID count and beacon overhead

Each SSID on each radio sends a beacon about every 102.4 ms (100 time units of 1.024 ms is the usual default interval; IEEE 802.11 is paywalled, gated: unconfirmed, source is paywalled or blocked) at the lowest basic rate. Every AP
the client can hear on the same channel adds its beacons. On 2.4 GHz with 1 Mbps basic rate a
beacon takes ~2-3 ms of airtime.

## Rough overhead (2.4 GHz, 1 Mbps basic rate)
Computed as SSIDs x APs x beacon time / 102.4 ms, with a 192 us long preamble plus a 250-byte beacon at 1 Mbit/s = 2.19 ms (2.59 ms for 300 bytes). With 2.4 ms per beacon the table rows come to 21 %, 47 % and 94 %; with 2.6 ms, 23 %, 51 % and over 100 %. Beacon size varies with the information elements, so treat the table as an estimate.
| SSIDs | APs heard on channel | Beacon airtime |
|---|---|---|
| 3 | 3 | ~20 % |
| 5 | 4 | ~45 % |
| 8 | 5 | > 90 % (network unusable) |
At a 12 Mbps minimum rate the same beacon takes about 0.19-0.22 ms (roughly 11x less) and at 24 Mbps about 0.10-0.12 ms (assuming a 20 us OFDM preamble); on 5/6 GHz the lowest rate is 6 Mbps (gated: unconfirmed, source is paywalled or blocked).
Use an SSID overhead calculator for your numbers.

## Rules
- Aim for **3-4 SSIDs per radio maximum** (e.g. corporate, guest, IoT).
- Consolidate: one 802.1X SSID with RADIUS-assigned VLAN/role (staff, contractors, devices) instead
  of one SSID per department.
- IoT: one SSID with iPSK/MPSK and per-key VLANs.
- Disable legacy rates: minimum basic rate 12 Mbps (or 24) where clients allow; disable 802.11b.
- Disable 2.4 GHz on some APs in dense deployments; only broadcast SSIDs where needed
  (AP groups / tags).
- Hidden SSIDs still beacon (with null SSID) and cause probe floods; they do not save airtime.

## Verify
- [ ] Per channel: SSIDs x APs heard documented; channel utilisation from beacons alone (idle network) < 10 %.
