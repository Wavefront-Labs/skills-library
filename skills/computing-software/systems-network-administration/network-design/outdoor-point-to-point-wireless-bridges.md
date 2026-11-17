---
id: computing-software.systems-network-administration.network-design.outdoor-point-to-point-wireless-bridges
name: outdoor-point-to-point-wireless-bridges
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, point-to-point-wireless, ptp-link, fresnel-zone, link-budget, wireless-bridge]
level: practitioner
status: gated
description: "Plan an outdoor point-to-point wireless bridge: line of sight and Fresnel clearance, frequency choice (5/6/60 GHz, licensed), link budget, alignment and monitoring."
sources:
  - https://www.itu.int/rec/R-REC-P.530
  - https://www.ui.com/airmax/
  - https://www.cambiumnetworks.com/products/ptp/
  - https://www.fcc.gov/wireless/bureau-divisions/broadband-division/microwave-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Outdoor point-to-point wireless bridges

## Frequency options
| Band | Range | Notes |
|---|---|---|
| 5 GHz unlicensed | long | crowded; DFS radar events cause outages |
| 6 GHz | varies by region | rules differ by region; check the local regulator |
| 60 GHz (V-band) | short | high capacity, narrow beams, rain/oxygen fade |
| 70/80 GHz (E-band) | medium | licensing rules vary, rain fade |
| Licensed 6-38 GHz microwave | long | coordinated, protected, carrier-grade |

## Path design
1. **Line of sight** plus most of the first Fresnel zone clear of obstacles (a common planning rule is 60 % clearance) (gated: unconfirmed, source is paywalled or blocked) (trees, roofs, terrain).
   First Fresnel radius at midpoint (m) ~ 8.66 x sqrt(D_km / f_GHz). 5 km at 5.8 GHz -> ~8 m radius.
2. Earth curvature matters beyond a few km: raise masts.
3. Account for tree growth and new buildings over the link's life.

## Link budget
Rx signal = Tx power + Tx gain - FSPL - losses + Rx gain.
FSPL (dB) = 20log10(d_km) + 20log10(f_MHz) + 32.44. Allow a fade margin; rain fade matters more at higher frequencies (see ITU-R P.530) (gated: unconfirmed, source is paywalled or blocked).

## Install
- Rigid mounts (wind sway kills narrow beams), align with the radio's tone/RSSI tool to the
  predicted signal, both ends.
- Ground the mast, surge protectors on the PoE cable at both building entries.
- Encrypt (AES) and isolate management.

## Operate
Monitor RSSI, SNR, modulation rate and errors via SNMP; alert on drops below planned values; an
alternative path (fibre, LTE) for critical sites.

## Verify
- [ ] Measured RSSI close to the prediction, expected modulation sustained, throughput test (iperf3) in both directions.

## Checked

- Date: 2026-10-28
- Confirmed: The Fresnel radius formula and the free-space path loss formula were checked by arithmetic (r = 17.3*sqrt(d1*d2/(f*D)) gives 8.66*sqrt(D/f) at midpoint; 5 km at 5.8 GHz gives about 8 m).
- Removed: range figures per band, AFC wording, 2-3 dB and 10-20 dB figures.
- Gated: the 60 % Fresnel clearance rule and the fade-margin guidance (ITU P.530 page was a summary stub).
Method: documentation only; no commands were run.
