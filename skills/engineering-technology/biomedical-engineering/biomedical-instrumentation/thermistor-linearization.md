---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.thermistor-linearization
name: thermistor-linearization
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [thermistor, temperature-sensing, respiratory-monitoring, ntc-thermistor, steinhart-hart, beta-equation, ratiometric-adc, self-heating, clinical-thermometer]
level: practitioner
status: gated
description: "Convert NTC thermistor readings to temperature accurately: beta and Steinhart-Hart equations, divider and ratiometric ADC design, self-heating and calibration."
sources: ["Steinhart and Hart, Calibration curves for thermistors (Deep-Sea Research 1968)", "ISO 80601-2-56 Clinical thermometers for body temperature measurement (confirm edition)", "ASTM E1112-00(2018) Electronic thermometer for intermittent determination of patient temperature (listed as withdrawn 14 May 2026 by BSI Knowledge)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Thermistor linearisation and accuracy

**Goal:** read body temperature with a thermistor to a few hundredths of a degree after calibration.

## Conversion
- **Beta model:** 1/T = 1/T0 + (1/B) ln(R/R0), T in kelvin, T0 = 298.15 K and R0 the resistance at 25 C, B in the order of 3000-4000 K (gated: unconfirmed, source is paywalled or blocked). A 3950 K, 10 kOhm part gives 5.99 kOhm at 37 C and the model returns 37.0 C (computed round trip). Accurate over a small range (for body temperature, say 30-45 C) when B is fitted over that range.
- **Steinhart-Hart:** 1/T = A + B ln R + C (ln R)^3 with three constants from three calibration points. Fits within a few millidegrees over wide ranges.
- Do the calculation in floating point or a lookup table with interpolation.

## Circuit
- Use a voltage divider with a precision reference resistor near the thermistor resistance at mid-range, and measure **ratiometrically** (ADC reference tied to the divider supply) so supply drift cancels.
- Choose R_ref to maximise sensitivity in the clinical range; add a parallel or series resistor to linearise coarsely if no processor.
- Use a 16-bit or better ADC for 0.01 C resolution, or a sigma-delta.

## Error sources
- **Self-heating:** P = I^2 R; with a dissipation constant of say 1 mW/C, 100 microwatts gives 0.1 C. Keep excitation low or pulse it.
- Thermistor tolerance and interchangeability: calibrate at two or three points against a reference thermometer in a stirred bath.
- Lead resistance and thermal mass; contact and conduction errors dominate clinical readings.
- Ageing and drift in epoxy-coated beads.

## Clinical standards
Clinical thermometers are covered by ISO 80601-2-56 (ASTM E1112-00(2018) is listed as withdrawn; check which standard your market applies), with accuracy limits across a defined range, for example the laboratory accuracy requirement near body temperature that the standard sets.

## Verify
- [ ] Bath calibration at 3 points with a traceable reference.
- [ ] Self-heating measured by varying excitation current.
- [ ] Residual error across 32-42 C within the intended spec.
