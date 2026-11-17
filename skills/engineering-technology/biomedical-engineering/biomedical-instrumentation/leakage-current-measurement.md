---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.leakage-current-measurement
name: leakage-current-measurement
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [leakage-current-test, electrical-safety, iec-60601-1, patient-electrical-safety, patient-leakage, touch-current, earth-leakage, measuring-device]
level: advanced
status: gated
description: "Measure earth, touch and patient leakage current per IEC 60601-1: measurement network, test conditions, single faults, limits by applied part type and meter requirements."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 clause 8.7 (leakage currents and patient auxiliary currents; confirm edition and limits)", "IEC 62353 Recurrent test and test after repair of medical electrical equipment", "Safety analyser manufacturer manuals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Leakage current measurement

**Goal:** measure leakage currents under normal and fault conditions and compare with the standard's limits.

Limits below are the commonly cited values from IEC 60601-1 3rd edition; confirm in the edition and national deviations that apply. Every figure in this skill (limits, measuring-device network, 110% supply, test voltages) is (gated: unconfirmed, source is paywalled or blocked).

## Measuring device
A network that simulates the body impedance and frequency response: a resistor of 1 kOhm in parallel with a series 10 kOhm and 0.015 microfarad (the IEC 60601-1 measuring device), with a true-RMS voltmeter of adequate bandwidth, calibrated; the safety analyser implements this.

## Limits (microamps unless noted)
| Current | Normal condition (NC) | Single fault (SFC) |
|---|---|---|
| Earth leakage | 5 mA | 10 mA |
| Touch current | 100 | 500 |
| Patient leakage, type B or BF | 100 | 500 |
| Patient leakage, type CF | 10 | 50 |

## Test conditions
1. Equipment at operating temperature, in all operating modes, at 110% of the highest rated supply voltage.
2. Normal polarity and reversed polarity of the supply.
3. **Single fault conditions:** open supply conductor (neutral), open protective earth, and for patient leakage a mains voltage on the signal input/output or applied-part tests per the standard (the standard lists the combinations).
4. Mains on applied part test (for F-type): 110% of mains voltage applied to the F-type applied part through a limiting resistor; limits are higher (for BF and CF) to reflect isolated design.
5. Measure from each accessible part and applied part to earth and between applied parts.

## Gotchas
- Safety analysers must be calibrated and configured to the right standard and applied-part type.
- Leakage depends on cable and accessories; test with the intended set.
- Y-capacitors and isolated converters set leakage; the design must allow margin.

## Verify
- [ ] All limit tests passed with margin (for example 50% of limit in NC).
- [ ] Recorded polarity, fault condition, applied part and result.
- [ ] Re-test after any design change in power or isolation.
