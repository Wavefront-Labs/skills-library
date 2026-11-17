---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.four-electrode-measurement
name: four-electrode-measurement
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [four-electrode, bioimpedance, impedance-measurement, tetrapolar, current-injection, auxiliary-current, impedance-spectroscopy]
level: advanced
status: gated
description: "Measure bioimpedance with four electrodes to remove contact impedance error: current source, voltage sense, geometry, frequency choice and IEC 60601 current limits."
sources: ["Grimnes and Martinsen, Bioimpedance and Bioelectricity Basics", "IEC 60601-1 patient auxiliary current limits (confirm values in the current edition)", "Webster (ed.), Medical Instrumentation: Application and Design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Four-electrode (tetrapolar) impedance measurement

**Goal:** measure tissue impedance without the electrode-skin impedance contaminating the result.

## Principle
- Two outer electrodes inject a known alternating current; two inner electrodes sense the voltage with a high-impedance amplifier that draws almost no current. Because no current flows in the sense leads, the contact impedance at the sense electrodes produces little voltage error.
- Z = V_sense / I_injected; geometry (electrode spacing and tissue cross-section) sets the conversion to resistivity.

## Design steps
1. **Current source:** a Howland or similar voltage-controlled current source with high output impedance (well above the expected skin plus tissue impedance) over the frequency range; check output impedance and compliance voltage.
2. **Frequency:** from about 1 kHz to 1 MHz for spectroscopy; 50 kHz is typical for single-frequency body composition (gated: unconfirmed, source is paywalled or blocked). Current limits rise with frequency.
3. **Current amplitude:** IEC 60601-1 limits patient auxiliary current for applied parts in the microamp range at DC and below 1 kHz (the DC limit is lower than the AC limit, so take the DC and AC values per applied-part type from the standard) and allows more above 1 kHz, rising with frequency up to a ceiling in the milliamp range (gated: unconfirmed, source is paywalled or blocked). Confirm exact values and type CF limits in the edition you apply.
4. **Sense amplifier:** instrumentation amplifier with input impedance of tens of megohms, low input capacitance, high CMRR.
5. **Demodulation:** synchronous detection to get amplitude and phase (see lock-in-demodulation).
6. **Geometry:** electrodes in a line with equal spacing for local measurements; use ring or band electrodes for limb segments.

## Error sources
- Stray capacitance and cable capacitance give frequency-dependent errors above about 100 kHz; use shielded, short leads and active shields.
- Current paths do not follow the straight line; skin, fat and bone redirect current.
- Unequal electrode contact causes common-mode conversion.

## Verify
- [ ] Calibrate with precision resistor networks and an R-C test cell across the band.
- [ ] Measure injected current to stay inside the limits in fault conditions too.
- [ ] Repeatability on the same subject with electrode re-application.
