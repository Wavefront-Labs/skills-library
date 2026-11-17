---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.capnography-principles
name: capnography-principles
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [capnography, temperature-sensing, respiratory-monitoring, temperature-respiratory-sensing, ndir, end-tidal-co2, sidestream, mainstream, iso-80601-2-55]
level: practitioner
status: gated
description: "Understand capnography: NDIR CO2 measurement at 4.26 microns, mainstream versus sidestream designs, waveform phases, accuracy factors, calibration and ISO 80601-2-55 context."
sources: ["ISO 80601-2-55 Particular requirements for the basic safety and essential performance of respiratory gas monitors (confirm edition)", "Gravenstein, Jaffe and Paulus, Capnography: Clinical Aspects", "Webster (ed.), Medical Instrumentation: Application and Design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Capnography principles

**Goal:** measure carbon dioxide concentration in respiratory gas breath by breath and display the capnogram and end-tidal value.

Every figure in this skill (4.26 micrometre band, 50-200 mL/min sample flow, ISO 80601-2-55 limits) is (gated: unconfirmed, source is paywalled or blocked). The mmHg-to-kPa conversion was computed: 35-45 mmHg is 4.67-6.00 kPa.

## Measurement principle
CO2 absorbs infrared light strongly near 4.26 micrometres. **Non-dispersive infrared (NDIR)** sensors pass IR through the sample, then through a narrow band-pass filter at the CO2 band onto a detector; absorption follows the Beer-Lambert law. A reference channel (another wavelength with no CO2 absorption) compensates for source ageing and window contamination. Other techniques include micro-stream (sidestream) designs with small cells and photoacoustic or colorimetric indicators for simple use.

## Configurations
- **Mainstream:** the sensor sits on the airway adapter at the patient's airway; fast response, no sample lag, but adds weight and dead space, and heated windows prevent condensation.
- **Sidestream:** a sampling line draws gas (typically 50-200 mL/min) to a remote sensor; suited to non-intubated patients with nasal cannulas; has transport delay (a second or two), water traps or Nafion tubes to manage humidity, and needs gas return or scavenging.

## Capnogram and values
- Phases: I (dead space gas, near zero), II (rapid upstroke), III (alveolar plateau), then inspiration. **End-tidal CO2 (etCO2)** is the value at the end of the plateau; normal around 35-45 mmHg (about 4.7-6.0 kPa) for healthy adults, usually slightly below arterial CO2.
- The waveform shape shows apnoea, rebreathing, obstruction, cardiac oscillations and intubation checks.

## Accuracy factors
- Cross-sensitivity to nitrous oxide, oxygen and anaesthetic agents (collision broadening) is compensated by user-entered gas composition or by agent sensors.
- Pressure and temperature effects: calibrate or compensate for barometric pressure; water vapour reduces measured partial pressure.
- Response time: rise time and sample delay matter at high respiratory rates in neonates.
- Calibration with a certified CO2 gas (for example 5% CO2) at set intervals; zeroing against room air or a CO2-free gas.

## Standard
ISO 80601-2-55 sets requirements for accuracy, rise time, alarms and performance of gas monitors (confirm the edition and numeric limits).

## Verify
- [ ] Accuracy at several CO2 levels with a gas mixer and certified gases.
- [ ] Rise time and delay time measured with a fast valve step.
- [ ] Alarm functions (apnoea, high and low etCO2) tested against the standard.
