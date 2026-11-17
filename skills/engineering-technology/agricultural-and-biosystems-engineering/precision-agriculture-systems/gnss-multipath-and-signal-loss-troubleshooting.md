---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.gnss-multipath-and-signal-loss-troubleshooting
name: gnss-multipath-and-signal-loss-troubleshooting
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, gnss-multipath, gnss-positioning, rtk-gnss, signal-loss, hdop, antenna-placement, rtk-float]
level: practitioner
status: draft
description: "Diagnose GNSS errors in the field: multipath, canopy and terrain masking, antenna placement, satellite geometry, interference and ionosphere, with a stepwise checklist."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# GNSS multipath and signal loss troubleshooting

**Goal:** find why position is noisy, floats or drops out, and fix it.

## Checklist
1. **Status display**: satellites tracked, HDOP (below about 2 is good), correction age, RTK fixed or float, signal strength (C/N0).
2. **Antenna**: on the cab roof or a mast with a ground plane, clear 360 degree sky view, away from reflective metal (light bars, roof racks); secure cable and connectors; check for water in connectors.
3. **Multipath**: reflections from buildings, machines and wet ground produce erratic jumps; move the antenna, use a choke-ring or multipath-resistant antenna, raise the elevation mask (for example 10-15 degrees).
4. **Obstructions**: tree rows, shelterbelts, hills and buildings reduce satellites and break RTK fix; plan headland turns where there is sky; use multi-constellation receivers (GPS, GLONASS, Galileo, BeiDou) to improve availability.
5. **Corrections**: age and latency of RTK corrections, radio signal quality, NTRIP connection or cellular strength; switch to a fallback (SBAS) if lost.
6. **Interference**: poorly shielded electronics, radio transmitters or jammers; test the receiver away from the source.
7. **Ionosphere and solar activity**: periods of storm degrade RTK fix; check space weather forecasts when accuracy suddenly falls without a local cause.
8. **Receiver settings**: dynamics model, antenna type, offsets, firmware.

## Gotchas
- A changed antenna height or offset looks like a drift or a consistent offset on slopes.
- Do not diagnose with a single log; compare with a second receiver.

## Verify
- [ ] Re-test on the same track and confirm fix retention and cross-track error improved.
