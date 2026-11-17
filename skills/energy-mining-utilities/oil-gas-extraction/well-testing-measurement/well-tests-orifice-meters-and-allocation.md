---
id: energy-mining-utilities.oil-gas-extraction.well-testing-measurement.well-tests-orifice-meters-and-allocation
name: well-tests-orifice-meters-and-allocation
category: energy-mining-utilities
field: oil-gas-extraction
product: well-testing-measurement
tags: [well-testing-measurement, well-test, production-test, test-separator, flow-test, orifice-meter, orifice-plate, differential-pressure, efm, electronic-flow-meter, flow-computer, chart-recorder, aga-3, coriolis-meter, turbine-meter, custody-transfer, lact, meter-proving, meter-factor, fluid-sampling, gas-sampling, gas-chromatograph, allocation, production-allocation, back-allocation, gor, water-cut, measurement-technician]
level: practitioner
status: draft
description: "Measure what wells make: running a well test through a test separator, orifice meter checks and chart/EFM data, sampling, and allocating battery sales back to wells."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Well tests, orifice meters and allocation

**Goal:** produce well rates and sales volumes that are accurate enough to manage the
field and defensible enough to pay royalties and partners on.

> Status: draft. Standards referenced (AGA Report No. 3 for orifice metering, API MPMS
> for liquids) are the common North American ones; regulators and contracts specify
> which apply and how often tests and calibrations happen.

## 1. Running a well test
- Route one well to the **test separator** while the others produce to the group
  separator. Let it **stabilise** — after switching, flow and pressures need time
  (hours for many wells) before the test is representative; record stabilisation.
- Measure oil, water and gas rates over a test period (often 24 h), along with
  tubing/casing pressure, choke size, and separator pressure and temperature.
- Calculate **water cut** (water ÷ total liquid) and **GOR** (gas ÷ oil). Compare
  with previous tests; a sudden change is either the well or the test equipment.
- Tests are only as good as the test separator meters — check them like custody meters.

## 2. Orifice meters
- Flow is calculated from **differential pressure** across a sharp-edged plate, static
  pressure, temperature, and gas composition (via the flow computer per AGA-3).
- Common errors:
  - **Plate installed backwards** (bevel upstream) — reads low by several percent.
  - Damaged or dirty plate edge, bowed plate.
  - Wrong plate size entered in the flow computer after a plate change.
  - **Liquids in gas lines** or blocked impulse lines distort DP.
  - DP very low in the transmitter range (poor accuracy) — consider changing plate size
    so normal flow sits in the useful part of the range.
- **Inspections/calibrations:** pull and inspect the plate, check bore against the
  stamp, calibrate DP, static and temperature transmitters; record "as found / as left".
- Old-style **chart recorders**: change charts on time, ink pens working, clock running.

## 3. Liquid custody transfer
- LACT units and Coriolis meters are **proved** against a prover to establish a **meter
  factor**. Track meter factor history — a drifting factor signals wear or deposits.
- Samplers take flow-proportional samples for BS&W and gravity.

## 4. Sampling
- Gas samples (for composition, heating value, H₂S) into clean cylinders using the
  specified purge/fill method; liquid samples representative of flowing conditions.
- Label with date, time, point, pressure, temperature. A sample with no metadata is
  worthless.

## 5. Allocation
- Sales at the battery (measured) are shared back to wells using their test rates:
  well allocated volume = sales volume × (well test rate × days on ÷ Σ all wells' test
  rate × days on). Subtract fuel, flare and shrinkage per your method.
- Low-quality or old tests make allocation wrong for every well in the group — keep
  the test schedule.
- An **allocation factor** (sales ÷ sum of theoretical) far from 1 points at measurement
  problems somewhere.

## Gotchas
- Downtime hours entered wrongly distort allocation as much as a bad test.
- Flow computer configuration changes must be documented and approved — they move money.
- Temperature matters: liquid volumes are corrected to standard conditions.

## Verify
- [ ] Well stabilised before test; test duration and conditions recorded.
- [ ] Orifice plate orientation, size and configuration verified.
- [ ] Transmitter calibrations as-found/as-left recorded.
- [ ] Meter factors and samples current.
- [ ] Allocation factor within the expected range and explained if not.
