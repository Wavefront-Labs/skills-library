---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.sbas-and-satellite-delivered-corrections
name: sbas-and-satellite-delivered-corrections
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, sbas-corrections, gnss-positioning, rtk-gnss, waas, egnos, ppp, l-band-correction]
level: practitioner
status: draft
description: "Use SBAS and satellite-delivered corrections (WAAS, EGNOS, subscription L-band, free high-accuracy services): coverage, convergence and when they fall short."
sources:
  - "EUSPA, Galileo High Accuracy Service (https://www.euspa.europa.eu/european-space/galileo/services/galileo-high-accuracy-service-has)"
  - "FAA WAAS (https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/waas)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SBAS and satellite-delivered corrections

**Goal:** decimetre to few-centimetre accuracy without a base station or cellular.

## Services
- **SBAS**: geostationary satellites broadcast corrections (WAAS in North America, EGNOS in Europe, MSAS in Japan, GAGAN in India). Free, no setup; accuracy depends on receiver and conditions (vendors quote pass-to-pass figures in the decimetre range; take the absolute accuracy from the SBAS operator's published performance, unconfirmed here), adequate for many spraying and general tasks.
- **Subscription satellite corrections** (L-band, commercial PPP-style services): corrections broadcast over geostationary satellites or the internet; accuracy of a few cm after a convergence period of tens of minutes; independent of cellular coverage.
- **Free high-accuracy services**: some constellations offer free precise-point-positioning corrections (for example the Galileo High Accuracy Service, described by EUSPA as free and globally available); availability, accuracy and receiver support change, so verify the current status and your receiver's capability.

## Practical points
1. **Convergence**: after power up or signal loss, PPP solutions need minutes to reach full accuracy; plan start-up before working.
2. **Datum**: satellite corrections are in a global reference frame (changing with tectonic drift each year), so lines recorded in one year may be offset next year; use fixed RTK for repeatable lines.
3. **Ionosphere**: solar activity and low-latitude regions degrade performance; check forecasts when accuracy matters.
4. Coverage: SBAS satellites sit at low elevation at high latitudes; trees and buildings block them.

## Verify
- [ ] Check position stability on a stationary receiver over 15-30 minutes after convergence; record drift.
