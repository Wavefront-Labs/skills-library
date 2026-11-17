---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.tyre-pressure-monitoring-system-design
name: tyre-pressure-monitoring-system-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [tpms, tyre-pressure-monitoring, tire-pressure-monitoring, direct-tpms, indirect-tpms, fmvss-138, un-r141, wheel-sensor, tyre-pressure, wheel-package]
level: practitioner
status: gated
description: "Design a TPMS: choose direct or indirect, pressure and temperature sensing, wheel localisation, calibration and learn procedures, and confirm FMVSS 138 or UN R141 requirements."
sources:
  - "FMVSS 138 (tire pressure monitoring systems) and UN Regulation 141 (TPMS); EU type-approval requirements; confirm current texts at https://unece.org"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "https://www.law.cornell.edu/cfr/text/49/571.138"
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.138"
  - "https://treaties.un.org/doc/Publication/MTDSG/Volume%20I/Chapter%20XI/XI-B-16-141.en.xml"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Tyre pressure monitoring system design

## 1. Regulatory context
Many markets require TPMS on new passenger cars: the US (FMVSS 138) and the EU and countries applying UN Regulation No. 141 (TPMS; in force 22 January 2017; it was split out of UN R64, which keeps the spare-wheel and run-flat provisions). FMVSS 138 (49 CFR 571.138) requires the telltale within 20 minutes once one or more tyres (up to four) are at or below 25 percent under the recommended cold pressure or the Table 1 minimum activation pressure, whichever is higher, and a malfunction warning within 20 minutes of a fault. UN R141 thresholds, test conditions and times differ; confirm the current text and your market before fixing requirements.

## 2. Direct TPMS
A battery-powered sensor in each wheel (on the valve or strapped to the rim) measures pressure and usually temperature, accelerometer-based motion detection, and sends a radio frame (typical bands include around 315 MHz and 433 MHz depending on region (gated: unconfirmed, source is paywalled or blocked)) to a vehicle receiver.
- Accurate absolute pressure; works for slow leaks and all four tyres.
- Sensor battery life (several years), service tool required, sensor mass affects wheel balance, extra cost; winter wheel sets need their own sensors.
- Localisation (which wheel): by low-frequency trigger, by RSSI, or by wheel-speed/accelerometer phase correlation with ABS signals.

## 3. Indirect TPMS
Uses ABS wheel-speed sensors. Under-inflation reduces rolling radius (the wheel spins faster) and changes the vibration spectrum of the wheel speed signal. Algorithms detect relative differences and spectral shifts. No wheel hardware, low cost; but relative (needs a reset or learn after inflation), it may not detect all four tyres losing pressure equally except with spectral methods, and has slower detection. Choice of method must satisfy the regulation's detection scenarios.

## 4. System design points
- **Thresholds:** warn below a threshold relative to placard pressure (regulation-defined), add temperature compensation to a cold-pressure reference.
- **Reset and learn:** after tyre changes and rotation.
- **Driver interface:** telltale, message, per-tyre pressure display.
- **Diagnostics:** sensor battery low, missing sensor, receiver faults, RF interference.
- **Interaction:** with ABS/ESC for indirect systems, and spare wheel or run-flat.
- **Validation:** vehicle tests of puncture and slow-leak scenarios under the regulatory procedure, EMC and RF tests.

## Verify
- [ ] Applicable regulation and thresholds confirmed for each market.
- [ ] Method (direct or indirect) covers required detection scenarios.
- [ ] Learn, reset and winter wheel procedures defined.
- [ ] RF, EMC and sensor life validated.
