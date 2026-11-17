---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.rtk-base-station-and-network-rtk-setup
name: rtk-base-station-and-network-rtk-setup
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, rtk-base-station, gnss-positioning, rtk-gnss, base-station, radio-link, network-rtk, baseline-length]
level: practitioner
status: draft
description: "Set up an RTK base or network RTK: base site, coordinates, radio link, baseline limits, mobile receiver configuration and checks of fixed status and repeatability."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RTK base station and network RTK setup

**Goal:** centimetre-level corrections that are stable and repeatable.

## Own base station
1. **Site**: clear view of the sky, away from reflective surfaces and tall trees, on a stable mount (a pillar or fixed building, not a wobbling tripod), power with backup, and antenna height recorded.
2. **Coordinates**: either enter a known coordinate (survey mark) or average a long observation; for repeatable positions, keep the same coordinates every season and note the datum.
3. **Radio link**: UHF (typically 450 MHz band in many regions) or spread-spectrum 900 MHz or 2.4 GHz; a high mast raises range; follow local licence rules for frequency and power.
4. **Baseline**: RTK accuracy degrades with distance from the base (commonly about 1 ppm, i.e. 1 mm per km; confirm in the receiver datasheet) and fix reliability falls beyond about 10-20 km.
5. Check that the rover receives the correct message type and rate (RTCM 3.x or the manufacturer's format).

## Network RTK
Subscribe to a regional network that provides corrections over cellular data using NTRIP (see that skill); the network gives a virtual base near the rover; requires mobile coverage along the whole farm.

## Checks
- Status shows "RTK fixed" (not "float") in the rover; check satellite count and HDOP.
- Verify a known point: drive to a survey mark or repeat a stake position and measure the offset.

## Gotchas
- Moving the base by even a few cm shifts all lines by that amount; record settings.
- Radio interference and trees limit range.

## Verify
- [ ] Rover remains fixed for the whole working area and returns to the surveyed mark within 2-3 cm.
