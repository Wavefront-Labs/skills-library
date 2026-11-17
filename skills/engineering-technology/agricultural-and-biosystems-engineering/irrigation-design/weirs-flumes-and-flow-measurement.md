---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.weirs-flumes-and-flow-measurement
name: weirs-flumes-and-flow-measurement
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, flow-measurement-weir, v-notch-weir, parshall-flume, cipolletti, open-channel-flow-meter, flow-measurement]
level: practitioner
status: gated
description: "Measure irrigation flow with weirs, flumes and meters: selection, installation rules, head measurement, free versus submerged flow and field accuracy checks."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Weirs, flumes and flow measurement

**Goal:** measured flow within a known accuracy for scheduling, water accounting and calibration of other tests.

## Devices
- Sharp-crested weirs: 90-degree V-notch for small flows (Q is about 1.38 x H^2.5 in m3/s with head H in m; this agrees within about 2.5% with the USBR Water Measurement Manual Eq. 7-6, Q = 2.49 h^2.48 in ft3/s and ft, over heads of 0.25 to 1.25 ft. USBR limits: discharges 0.05 to 4.25 ft3/s, head above 0.2 ft, notch edges at least 2 h_max from the approach boundaries), rectangular and Cipolletti weirs for larger flows. Require free fall below the crest and a still approach pool.
- Flumes: Parshall, cutthroat and Replogle flumes; Parshall flumes have standard throat sizes and rating tables (gated: unconfirmed, source is paywalled or blocked). USBR states flumes lose much less head than sharp-crested weirs (about a quarter or less) and can be designed to limit sediment deposition.
- Orifices and gated turnouts with calibrated gates; propeller, magnetic and ultrasonic meters in pipelines (require straight pipe before and after, per the manufacturer).

## Rules
- Measure head at the specified distance upstream of the crest or throat with a staff gauge or logger.
- Keep the approach pool clean and free of velocity; check zero by the crest elevation.
- Know the submergence limit; above it, a correction is needed or the rating breaks.
- Document the standard (ISO and ASTM methods exist for weirs and flumes; current designations not confirmed here (gated: unconfirmed, source is paywalled or blocked)) and the rating table in use.

## Check
Cross-check against a volumetric measurement at small flows or with a current meter at large flows.

## Verify
- [ ] Rating curve source recorded; zero and head location checked.
- [ ] Free-flow condition confirmed each reading.
- Use the rating from the standard or the USBR manual rather than a rounded coefficient.
