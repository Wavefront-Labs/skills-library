---
id: computing-software.systems-network-administration.network-design.wifi-site-survey-and-coverage-targets
name: wifi-site-survey-and-coverage-targets
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, wifi-design, site-survey, predictive-survey, ap-on-a-stick, validation-survey, rssi, snr, coverage-targets, ekahau, hamina, wall-attenuation, voice-grade-wifi, high-density-wifi, airtime]
level: practitioner
status: draft
description: "Run predictive, AP-on-a-stick and validation Wi-Fi surveys with design targets: -67 dBm primary, SNR 25 dB, secondary coverage for roaming, wall attenuation, capacity per AP."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Mobility/vowlan/41dg/vowlan41dg-book.html
  - https://www.ekahau.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wi-Fi site surveys and coverage targets

## Design targets (set them before surveying)
| Requirement | Data/web | Voice / real-time | Location/RTLS |
|---|---|---|---|
| Primary RSSI | -70 dBm | **-67 dBm** | -67 dBm from 3+ APs |
| Secondary RSSI (2nd AP) | n/a | -70 to -75 dBm (for roaming) | n/a |
| SNR | 20 dB | 25 dB | 25 dB |
| Co-channel APs heard > -85 dBm | <= 2 | <= 1-2 | |
| Retries | < 15% | < 10% | |
Targets come from the **client** perspective: survey with a device similar to the weakest client
(phones, scanners), and use the 5 GHz or 6 GHz band as the design band.

## Survey types
1. **Predictive**: floor plans in Ekahau/Hamina/iBwave, scaled, walls drawn with materials
   (drywall ~3 dB, brick ~10 dB, concrete 12-20 dB, elevator shafts/metal ~25+ dB, glass with
   coatings can be high). Place APs to meet targets; output BOM and mounting map.
2. **AP-on-a-stick** (pre-deployment): mount a real AP at planned height/power in representative
   areas, measure cell edges. Validates wall losses, warehouses, hospitals, anything unusual.
3. **Validation / post-install**: walk the whole space with the survey tool (passive for RSSI/SNR/
   co-channel, active for throughput/roaming/latency); compare against targets; adjust power,
   channels, add/move APs.
4. **Spectrum analysis** during surveys: find non-Wi-Fi interferers (microwaves, video senders,
   Bluetooth-heavy areas, DECT in some regions).

## Capacity, not just coverage
- Estimate devices per area x devices per person x simultaneous active share, apps' throughput;
  a 5 GHz 20/40 MHz radio comfortably serves ~30-50 active clients.
- Auditoriums/lecture halls: directional antennas, under-seat or ceiling mounts, 20 MHz widths,
  more APs at lower power.

## Practical gotchas
- Mount height above ~4-5 m (warehouses) changes coverage shape: use downtilt/directional antennas.
- Surveys done empty differ from occupied (people absorb ~3-5 dB); add margin.
- Record AP MAC/name to location during installation; validation is impossible otherwise.

## Verify
- [ ] Validation heatmaps for primary RSSI, SNR, secondary coverage and co-channel meet the targets per area.
- [ ] Roaming test walk with a voice call shows no drops.
